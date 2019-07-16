from collections import defaultdict

from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres import fields as postgres
from django.db import models
from allauth.account.models import EmailAddress
from simple_history.models import HistoricalRecords

from api.countries import COUNTRY_CHOICES
from api.oar_id import make_oar_id
from api.constants import Affiliations, Certifications


class EmailAsUsernameUserManager(BaseUserManager):
    """
    A custom user manager which uses emails as unique identifiers for auth
    instead of usernames.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Contributor(models.Model):
    """
    A participant in or observer of the supply chain that will
    upload facility lists to the registry.
    """
    # These choices must be kept in sync with the identical list kept in the
    # React client's constants file
    OTHER_CONTRIB_TYPE = 'Other'

    CONTRIB_TYPE_CHOICES = (
        ('Auditor', 'Auditor'),
        ('Brand/Retailer', 'Brand/Retailer'),
        ('Civil Society Organization', 'Civil Society Organization'),
        ('Factory / Facility', 'Factory / Facility'),
        ('Manufacturing Group / Supplier / Vendor',
         'Manufacturing Group / Supplier / Vendor'),
        ('Multi Stakeholder Initiative', 'Multi Stakeholder Initiative'),
        ('Researcher / Academic', 'Researcher / Academic'),
        ('Service Provider', 'Service Provider'),
        ('Union', 'Union'),
        (OTHER_CONTRIB_TYPE, OTHER_CONTRIB_TYPE),
    )

    admin = models.OneToOneField(
        'User',
        on_delete=models.PROTECT,
        help_text=('The user account responsible for uploading and '
                   'maintaining facility lists for the contributor'))
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The full name of the contributor.')
    description = models.TextField(
        null=False,
        blank=True,
        help_text='A detailed description of the contributor.')
    website = models.URLField(
        null=False,
        blank=True,
        help_text='A URL linking to a web site for the contributor.')
    contrib_type = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        choices=CONTRIB_TYPE_CHOICES,
        help_text='The category to which this contributor belongs.')
    other_contrib_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Free text field if selected contributor type is other'
    )
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text=(
            'Has this contributor has been verified by OAR staff.'
        ),
    )
    verification_notes = models.TextField(
        null=False,
        blank=True,
        help_text=(
            'A description of the manual steps taken to verify the '
            'contributor.'
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{name} ({id})'.format(**self.__dict__)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = EmailAsUsernameUserManager()

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        help_text='Unique email address used as a username'
    )
    username = models.CharField(max_length=20, null=True, blank=True)
    should_receive_newsletter = models.BooleanField(
        default=False,
        help_text='User has asked to receive the newsletter'
    )
    has_agreed_to_terms_of_service = models.BooleanField(
        default=False,
        help_text='User has agreed to the terms of service'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def first_name(self):
        pass

    def last_name(self):
        pass

    @property
    def did_register_and_confirm_email(self):
        try:
            email_address = EmailAddress.objects.get_primary(self.id)

            if email_address:
                return email_address.verified

        # if no EmailAddress record exists, the User was created through the
        # Django admin rather than the UI. Treat this User as verified.
            return True
        except EmailAddress.DoesNotExist:
            return True


class FacilityList(models.Model):
    """
    Metadata for an uploaded list of facilities.
    """
    contributor = models.ForeignKey(
        'Contributor',
        null=True,
        on_delete=models.SET_NULL,
        help_text='The contributor that uploaded this list.')
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The name of list. Defaults to name of the uploaded file.')
    description = models.TextField(
        null=True,
        blank=True,
        help_text='The description of list.')
    file_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        editable=False,
        help_text='The full name of the uploaded file.')
    header = models.TextField(
        null=False,
        blank=False,
        editable=False,
        help_text='The header row of the uploaded CSV.')
    is_active = models.BooleanField(
        null=False,
        default=True,
        help_text=('True if this list is current and has not been replaced '
                   'by another list'))
    is_public = models.BooleanField(
        null=False,
        default=True,
        help_text=('True if the public can see factories from this list '
                   'are associated with the contributor.'))
    replaces = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        unique=True,
        on_delete=models.PROTECT,
        help_text=('If not null this list is an updated version of the '
                   'list specified by this field.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1} ({2})'.format(
            self.contributor.name, self.name, self.id)


class FacilityListItem(models.Model):
    """
    Data, metadata, and workflow status and results for a single line from a
    facility list file.
    """
    UPLOADED = 'UPLOADED'
    PARSED = 'PARSED'
    GEOCODED = 'GEOCODED'
    GEOCODED_NO_RESULTS = 'GEOCODED_NO_RESULTS'
    MATCHED = 'MATCHED'
    POTENTIAL_MATCH = 'POTENTIAL_MATCH'
    CONFIRMED_MATCH = 'CONFIRMED_MATCH'
    ERROR = 'ERROR'
    ERROR_PARSING = 'ERROR_PARSING'
    ERROR_GEOCODING = 'ERROR_GEOCODING'
    ERROR_MATCHING = 'ERROR_MATCHING'
    DELETED = 'DELETED'

    # NEW_FACILITY is a meta status. If the `status` of a `FacilityListItem` is
    # `MATCHED` or `CONFIRMED_MATCH` and the `facility` was `created_from` the
    # `FacilityListItem` then the item represents a new facility.
    NEW_FACILITY = 'NEW_FACILITY'

    # REMOVED is also a meta status. A `FacilityListItem` has been removed if
    # any of its `FacilityMatch`es have `is_active` set to False.
    REMOVED = 'REMOVED'

    # These status choices must be kept in sync with the client's
    # `facilityListItemStatusChoicesEnum`.
    STATUS_CHOICES = (
        (UPLOADED, UPLOADED),
        (PARSED, PARSED),
        (GEOCODED, GEOCODED),
        (GEOCODED_NO_RESULTS, GEOCODED_NO_RESULTS),
        (MATCHED, MATCHED),
        (POTENTIAL_MATCH, POTENTIAL_MATCH),
        (CONFIRMED_MATCH, CONFIRMED_MATCH),
        (ERROR, ERROR),
        (ERROR_PARSING, ERROR_PARSING),
        (ERROR_GEOCODING, ERROR_GEOCODING),
        (ERROR_MATCHING, ERROR_MATCHING),
        (DELETED, DELETED),
    )

    ERROR_STATUSES = [ERROR, ERROR_PARSING, ERROR_GEOCODING, ERROR_MATCHING]

    class Meta:
        indexes = [
            models.Index(fields=['facility_list', 'row_index'],
                         name='api_fli_facility_list_row_idx'),
        ]

    facility_list = models.ForeignKey(
        'FacilityList',
        on_delete=models.CASCADE,
        help_text='The list that this line item is a part of.')
    row_index = models.IntegerField(
        null=False,
        editable=False,
        help_text='Index of this line in the CSV file.')
    raw_data = models.TextField(
        null=False,
        blank=False,
        help_text='The full, unparsed CSV line as it appeared in the file.')
    status = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        choices=STATUS_CHOICES,
        default=UPLOADED,
        help_text='The current workflow progress of the line item.')
    processing_started_at = models.DateTimeField(
        null=True,
        help_text=('When background processing of this item started. '
                   'Items awaiting processing will have a null value.'))
    processing_completed_at = models.DateTimeField(
        null=True,
        help_text=('When background processing of this item finished. '
                   'Items awaiting or in process will have a null value.'))
    processing_results = postgres.JSONField(
        default=list,
        help_text=('Diagnostic details logged by background processing '
                   'including details returned from the geocoder.'))
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The name of the facility taken from the raw data.')
    address = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The address of the facility taken from the raw data.')
    country_code = models.CharField(
        max_length=2,
        null=False,
        blank=False,
        choices=COUNTRY_CHOICES,
        help_text=('The ISO 3166-1 alpha-2 country code of the facility taken '
                   'directly from the raw data or looked up based on a full '
                   'country name provided in the raw data.'))
    geocoded_point = gis_models.PointField(
        null=True,
        help_text=('The geocoded location the facility address field taken '
                   'from the raw data.'))
    geocoded_address = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        help_text='The geocoded address of the facility.')
    facility = models.ForeignKey(
        'Facility',
        null=True,
        on_delete=models.PROTECT,
        help_text=('The facility created from this list item or the '
                   'previously existing facility to which this list '
                   'item was matched.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'FacilityListItem {id} - {status}'.format(**self.__dict__)


class FacilityClaim(models.Model):
    """
    Data submitted from a user attempting to make a verified claim of a
    Facility to be evaluated by OAR moderators.
    """
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'

    PREFERRED_CONTACT_CHOICES = (
        (EMAIL, EMAIL),
        (PHONE, PHONE),
    )

    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DENIED = 'DENIED'
    REVOKED = 'REVOKED'

    # These status choices must be kept in sync with the client's
    # `facilityClaimStatusChoicesEnum`.
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (APPROVED, APPROVED),
        (DENIED, DENIED),
        (REVOKED, REVOKED),
    )

    CUT_AND_SEW = 'Cut and Sew / RMG'
    DYEHOUSE = 'Dyehouse'
    EMBELLISHMENTS = 'Embellishments'
    FABRIC_MILL = 'Fabric Mill'
    FINISHING = 'Finishing'
    GINNING = 'Ginning'
    KNITTING = 'Knitting'
    LAUNDRY = 'Laundry'
    PACKING = 'Packing'
    SCOURING = 'Scouring'
    SCREENPRINTING = 'Screenprinting'
    STITCHING = 'Stitching (Shoes)'
    TANNERY = 'Tannery'
    WAREHOUSE = 'Warehouse'
    WEAVING = 'Weaving'
    OTHER = 'Other'

    FACILITY_TYPE_CHOICES = (
        (CUT_AND_SEW, CUT_AND_SEW),
        (DYEHOUSE, DYEHOUSE),
        (EMBELLISHMENTS, EMBELLISHMENTS),
        (FABRIC_MILL, FABRIC_MILL),
        (FINISHING, FINISHING),
        (GINNING, GINNING),
        (KNITTING, KNITTING),
        (LAUNDRY, LAUNDRY),
        (PACKING, PACKING),
        (SCOURING, SCOURING),
        (SCREENPRINTING, SCREENPRINTING),
        (STITCHING, STITCHING),
        (TANNERY, TANNERY),
        (WAREHOUSE, WAREHOUSE),
        (WEAVING, WEAVING),
        (OTHER, OTHER),
    )

    AFFILIATION_CHOICES = [
        (choice, choice)
        for choice in
        [
            Affiliations.BENEFITS_BUSINESS_WORKERS,
            Affiliations.BETTER_MILLS_PROGRAM,
            Affiliations.BETTER_WORK,
            Affiliations.CANOPY,
            Affiliations.ETHICAL_TRADING_INITIATIVE,
            Affiliations.FAIR_LABOR_ASSOCIATION,
            Affiliations.FAIR_WEAR_FOUNDATION,
            Affiliations.SEDEX,
            Affiliations.SOCIAL_LABOR_CONVERGENCE_PLAN,
            Affiliations.SUSTAINABLE_APPAREL_COALITION,
            Affiliations.SWEATFREE_PURCHASING_CONSORTIUM,
        ]
    ]

    CERTIFICATION_CHOICES = [
        (choice, choice)
        for choice in
        [
            Certifications.BCI,
            Certifications.B_CORP,
            Certifications.BLUESIGN,
            Certifications.CANOPY,
            Certifications.CRADLE_TO_CRADLE,
            Certifications.EU_ECOLABEL,
            Certifications.FSC,
            Certifications.GLOBAL_RECYCLING_STANDARD,
            Certifications.GOTS,
            Certifications.GREEN_SCREEN,
            Certifications.HIGG_INDEX,
            Certifications.IMO_CONTROL,
            Certifications.INTERNATIONAL_WOOL_TEXTILE,
            Certifications.ISO_9000,
            Certifications.IVN_LEATHER,
            Certifications.LEATHER_WORKING_GROUP,
            Certifications.NORDIC_SWAN,
            Certifications.OEKO_TEX_STANDARD,
            Certifications.OEKO_TEX_STEP,
            Certifications.OEKO_TEX_ECO_PASSPORT,
            Certifications.OEKO_TEX_MADE_IN_GREEN,
            Certifications.PEFC,
            Certifications.REACH,
            Certifications.RESPONSIBLE_DOWN_STANDARD,
            Certifications.RESPONSIBLE_WOOL_STANDARD,
            Certifications.SAB8000,
        ]
    ]

    contributor = models.ForeignKey(
        'Contributor',
        null=False,
        on_delete=models.PROTECT,
        help_text='The contributor who submitted this facility claim')
    facility = models.ForeignKey(
        'Facility',
        null=False,
        on_delete=models.PROTECT,
        help_text='The facility for which this claim has been submitted')
    contact_person = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='contact person',
        help_text='The contact person for the facility claim')
    job_title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The contact person\'s job title',
        verbose_name='contact person\'s job title',
        default='')
    email = models.EmailField(
        null=False,
        blank=False,
        verbose_name='email',
        help_text='The contact email for the facility claim')
    phone_number = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='phone number',
        help_text='The contact phone number for the facility claim')
    company_name = models.CharField(
        max_length=200,
        null=False,
        blank=True,
        verbose_name='company name',
        help_text='The company name for the facility')
    website = models.CharField(
        max_length=200,
        null=False,
        blank=True,
        verbose_name='website',
        help_text='The website for the facility')
    facility_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='description',
        help_text='A description of the facility')
    linkedin_profile = models.URLField(
        null=False,
        blank=True,
        help_text='A LinkedIn profile for verifying the facility claim',
        verbose_name='verification LinkedIn profile')
    verification_method = models.TextField(
        null=False,
        blank=True,
        verbose_name='verification method',
        help_text='An explanation of how the facility can be verified')
    preferred_contact_method = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        choices=PREFERRED_CONTACT_CHOICES,
        verbose_name='preferred contact method',
        help_text='The preferred contact method: email or phone')
    status = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name='status',
        help_text='The current status of this facility claim')
    status_change_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name='status change reason',
        help_text='The reason entered when changing the status of this claim.')
    status_change_by = models.ForeignKey(
        'User',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='status changed by',
        help_text='The user who changed the status of this facility claim',
        related_name='approver_of_claim')
    status_change_date = models.DateTimeField(
        null=True,
        verbose_name='status change date',
    )
    facility_name_english = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='The editable official English facility name for the claim.',
        verbose_name='facility name in English')
    facility_name_native_language = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='The editable official native language facility name.',
        verbose_name='facility name in native language')
    facility_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='address',
        help_text='The editable facility address for this claim.')
    facility_phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='facility phone number',
        help_text='The editable facility phone number for this claim.')
    facility_phone_number_publicly_visible = models.BooleanField(
        null=False,
        default=False,
        verbose_name='is facility phone number publicly visible',
        help_text='Is the editable facility phone number publicly visible?')
    facility_website = models.URLField(
        null=True,
        blank=True,
        verbose_name='facility website',
        help_text='The editable facility website for this claim.')
    facility_website_publicly_visible = models.BooleanField(
        null=False,
        default=False,
        help_text='Is the website publicly visible?',
        verbose_name='facility website visible')
    facility_minimum_order_quantity = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='minimum order quantity',
        help_text='The editable facility min order quantity for this claim.')
    facility_average_lead_time = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='average lead time',
        help_text='The editable facilty avg lead time for this claim.')
    facility_workers_count = models.IntegerField(
        null=True,
        blank=True,
        help_text='The editable facility workers count for this claim.',
        verbose_name='facility workers count')
    facility_female_workers_percentage = models.IntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(0, 101)],
        help_text=('Integer value indicating the facility\'s percentage of '
                   'female workers.'),
        verbose_name='percentage of female workers')
    facility_affiliations = postgres.ArrayField(
        models.CharField(
            null=False,
            blank=False,
            choices=AFFILIATION_CHOICES,
            max_length=50,
            help_text='A group the facility is affiliated with',
            verbose_name='facility affiliation',
        ),
        null=True,
        blank=True,
        help_text='The facility\'s affiliations',
        verbose_name='facility affilations',
    )
    facility_certifications = postgres.ArrayField(
        models.CharField(
            null=False,
            blank=False,
            choices=CERTIFICATION_CHOICES,
            max_length=50,
            help_text='A certification the facility has achieved',
            verbose_name='facility certification',
        ),
        null=True,
        blank=True,
        help_text='The facility\'s certifications',
        verbose_name='facility certifications',
    )
    facility_type = models.CharField(
        max_length=len(CUT_AND_SEW),
        null=True,
        blank=True,
        choices=FACILITY_TYPE_CHOICES,
        help_text='The editable facility type for this claim.',
        verbose_name='facility type')
    other_facility_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Editable alternate text when facility type is OTHER.',
        verbose_name='description of other facility type')
    facility_product_types = postgres.ArrayField(
        models.CharField(
            null=False,
            blank=False,
            max_length=50,
            help_text='A product produced at the facility',
            verbose_name='product type',
        ),
        null=True,
        blank=True,
        help_text='The products produced at the facility',
        verbose_name='product types',
    )
    facility_production_types = postgres.ArrayField(
        models.CharField(
            null=False,
            blank=False,
            max_length=50,
            help_text='A production type associated with the facility',
            verbose_name='production type',
        ),
        null=True,
        blank=True,
        help_text='The production types associated with the facility',
        verbose_name='production types',
    )
    point_of_contact_person_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='contact person',
        help_text='The editable point of contact person name')
    point_of_contact_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='contact email',
        help_text='The editable point of contact email')
    point_of_contact_publicly_visible = models.BooleanField(
        null=False,
        default=False,
        verbose_name='is contact visible',
        help_text='Is the point of contact info publicly visible?')
    office_official_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='office official name',
        help_text='The editable office name for this claim.')
    office_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='office address',
        help_text='The editable office address for this claim.')
    office_country_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        choices=COUNTRY_CHOICES,
        verbose_name='office country code',
        help_text='The editable office country code for this claim.')
    office_phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='office phone number',
        help_text='The editable office phone number for this claim.')
    office_info_publicly_visible = models.BooleanField(
        null=False,
        default=False,
        verbose_name='is office publicly visible',
        help_text='Is the office info publicly visible?')
    parent_company = models.ForeignKey(
        'Contributor',
        related_name='parent_company',
        null=True,
        default=None,
        on_delete=models.PROTECT,
        verbose_name='parent company',
        help_text='The parent company of this facility claim.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    default_change_includes = (
        'facility_name_english',
        'facility_name_native_language',
        'facility_address',
        'facility_phone_number',
        'facility_website',
        'facility_minimum_order_quantity',
        'facility_average_lead_time',
        'facility_workers_count',
        'facility_female_workers_percentage',
        'facility_affiliations',
        'facility_certifications',
        'facility_product_types',
        'facility_production_types',
        'facility_type',
        'other_facility_type',
        'facility_description',
        'facility_minimum_order_quantity',
        'facility_average_lead_time',
        'point_of_contact_person_name',
        'point_of_contact_email',
        'office_official_name',
        'office_address',
        'office_country_code',
        'office_phone_number',
        'parent_company',
    )

    # A dictionary where the keys are field names and the values are predicate
    # functions that will be passed a FacilityClaim instance and should return
    # a boolean.
    change_conditions = defaultdict(
        lambda: lambda c: True,
        facility_phone_number=(
            lambda c: c.facility_phone_number_publicly_visible),
        facility_website=(
            lambda c: c.facility_website_publicly_visible),
        point_of_contact_person_name=(
            lambda c: c.point_of_contact_publicly_visible),
        point_of_contact_email=(
            lambda c: c.point_of_contact_publicly_visible),
        office_official_name=(
            lambda c: c.office_info_publicly_visible),
        office_address=(
            lambda c: c.office_info_publicly_visible),
        office_country_code=(
            lambda c: c.office_info_publicly_visible),
        office_phone_number=(
            lambda c: c.office_info_publicly_visible),
    )

    # A dictionary where the keys are field_names and the values are functions
    # that will be passed a FacilityClaim and should return a string
    change_value_serializers = defaultdict(
        lambda: lambda v: v,
        parent_company=lambda v: v and v.name,
        facility_affiliations=lambda v: ', '.join(v) if v is not None else '',
        facility_certifications=lambda v: ', '.join(v)
        if v is not None else '',
        facility_product_types=lambda v: ', '.join(v)
        if v is not None else '',
        facility_production_types=lambda v: ', '.join(v)
        if v is not None else '',
    )

    def get_changes(self, include=list(default_change_includes)):
        latest = self.history.latest()
        previous = latest.prev_record
        changes = None
        if previous is not None:
            for field in FacilityClaim._meta.fields:
                should_report_change_publicly = \
                    self.change_conditions[field.name](self)
                if field.name in include and should_report_change_publicly:
                    curr_value = self.change_value_serializers[field.name](
                        getattr(self, field.name))
                    prev_value = self.change_value_serializers[field.name](
                        getattr(previous.instance, field.name))
                    if curr_value != prev_value:
                        if changes is None:
                            changes = []
                        changes.append({
                            'name': field.name,
                            'verbose_name': field.verbose_name,
                            'previous': prev_value,
                            'current': curr_value,
                        })
        return changes


class FacilityClaimReviewNote(models.Model):
    """
    A note entered by an administrator when reviewing a FacilityClaim.
    """

    claim = models.ForeignKey(
        'FacilityClaim',
        null=False,
        on_delete=models.PROTECT,
        help_text='The facility claim for this note'
    )
    author = models.ForeignKey(
        'User',
        null=False,
        on_delete=models.PROTECT,
        help_text='The author of the facility claim review note')
    note = models.TextField(
        null=False,
        blank=False,
        help_text='The review note')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()


class Facility(models.Model):
    """
    An official OAR facility. Search results are returned from this table.
    """
    class Meta:
        verbose_name_plural = "facilities"

    id = models.CharField(
        max_length=32,
        primary_key=True,
        editable=False,
        help_text='The OAR ID of a facility.')
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The name of the facility.')
    address = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text='The full street address of the facility.')
    country_code = models.CharField(
        max_length=2,
        null=False,
        blank=False,
        choices=COUNTRY_CHOICES,
        help_text='The ISO 3166-1 alpha-2 country code of the facility.')
    location = gis_models.PointField(
        null=False,
        help_text='The lat/lng point location of the facility')
    created_from = models.OneToOneField(
        'FacilityListItem',
        null=False,
        on_delete=models.PROTECT,
        related_name='created_facility',
        help_text=('The original uploaded list item from which this facility '
                   'was created.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{name} ({id})'.format(**self.__dict__)

    def save(self, *args, **kwargs):
        if self.id == '':
            new_id = None
            while new_id is None:
                new_id = make_oar_id(self.country_code)
                if Facility.objects.filter(id=new_id).exists():
                    new_id = None
            self.id = new_id
        super(Facility, self).save(*args, **kwargs)

    def other_names(self):
        facility_list_item_matches = [
            FacilityListItem.objects.get(pk=pk)
            for (pk,)
            in self
            .facilitymatch_set
            .filter(status__in=[FacilityMatch.AUTOMATIC,
                                FacilityMatch.CONFIRMED,
                                FacilityMatch.MERGED])
            .filter(is_active=True)
            .values_list('facility_list_item')
        ]

        return {
            match.name
            for match
            in facility_list_item_matches
            if len(match.name) != 0
            and match.name is not None
            and match.name != self.name
            and match.facility_list.is_active
            and match.facility_list.is_public
        }

    def other_addresses(self):
        facility_list_item_matches = [
            FacilityListItem.objects.get(pk=pk)
            for (pk,)
            in self
            .facilitymatch_set
            .filter(status__in=[FacilityMatch.AUTOMATIC,
                                FacilityMatch.CONFIRMED,
                                FacilityMatch.MERGED])
            .filter(is_active=True)
            .values_list('facility_list_item')
        ]

        return {
            match.address
            for match
            in facility_list_item_matches
            if len(match.address) != 0
            and match.address is not None
            and match.address != self.address
            and match.facility_list.is_active
            and match.facility_list.is_public
        }

    def contributors(self):
        facility_list_item_matches = [
            FacilityListItem.objects.get(pk=pk)
            for (pk,)
            in self
            .facilitymatch_set
            .filter(status__in=[FacilityMatch.AUTOMATIC,
                                FacilityMatch.CONFIRMED,
                                FacilityMatch.MERGED])
            .filter(is_active=True)
            .order_by('updated_at')
            .values_list('facility_list_item')
        ]

        # Converting from a list back to a set ensures the items are distinct
        return list(set([
            match.facility_list
            for match
            in facility_list_item_matches
            if match.facility_list.is_active
            and match.facility_list.is_public
            and match.facility_list.contributor is not None
        ]))

    def get_created_from_match(self):
        return self.facilitymatch_set.filter(
            facility_list_item=self.created_from
        ).first()

    def get_other_matches(self):
        return self.facilitymatch_set.exclude(
            facility_list_item=self.created_from
        ).all()

    def get_approved_claim(self):
        return self.facilityclaim_set.filter(
            status=FacilityClaim.APPROVED).count() > 0


class FacilityMatch(models.Model):
    """
    Matches between existing facilities and uploaded facility list items.
    """
    class Meta:
        verbose_name_plural = "facility matches"

    PENDING = 'PENDING'
    AUTOMATIC = 'AUTOMATIC'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    MERGED = 'MERGED'

    # These values must stay in sync with the `facilityMatchStatusChoicesEnum`
    # in the client's constants.js file.
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (AUTOMATIC, AUTOMATIC),
        (CONFIRMED, CONFIRMED),
        (REJECTED, REJECTED),
        (MERGED, MERGED),
    )

    facility_list_item = models.ForeignKey(
        'FacilityListItem',
        on_delete=models.PROTECT,
        help_text='The list item being matched to an existing facility.')
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.PROTECT,
        help_text=('The existing facility that may match an uploaded list '
                   'item.'))
    results = postgres.JSONField(
        help_text='Diagnostic details from the matching process.')
    confidence = models.DecimalField(
        null=False,
        max_digits=5,
        decimal_places=2,
        default=0.0,
        help_text=('A numeric representation of how confident the app is that '
                   'the list item matches the existing facility. Larger '
                   'numbers are better.'))
    status = models.CharField(
        null=False,
        max_length=9,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text=('The current status of the match. AUTOMATIC if the '
                   'application made a match with high confidence. PENDING '
                   'if confirmation from the contributor admin is required. '
                   'CONFIRMED if the admin approves the match. REJECTED if '
                   'the admin rejects the match. Only one row for a given '
                   'and facility list item pair should have either AUTOMATIC '
                   'or CONFIRMED status'))
    is_active = models.BooleanField(
        null=False,
        default=True,
        help_text=('A facility match is_active if its associated list item '
                   'not been removed; when a list item is removed, this '
                   'field will be set to False.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.facility_list_item, self.facility,
                                        self.status)


class FacilityAlias(models.Model):
    """
    Links the OAR ID of a no longer existing Facility to another Facility
    """
    class Meta:
        verbose_name_plural = "facility aliases"

    MERGE = 'MERGE'
    DELETE = 'DELETE'

    REASON_CHOICES = (
        (MERGE, MERGE),
        (DELETE, DELETE),
    )

    oar_id = models.CharField(
        max_length=32,
        primary_key=True,
        editable=False,
        help_text=('The OAR ID of a no longer existent Facility which should '
                   'be redirected to a different Facility.'))
    facility = models.ForeignKey(
        'Facility',
        null=False,
        on_delete=models.PROTECT,
        help_text='The facility now associated with the oar_id'
    )
    reason = models.CharField(
        null=False,
        max_length=6,
        choices=REASON_CHOICES,
        help_text='The reason why this alias was created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{} -> {}'.format(self.oar_id, self.facility)


class RequestLog(models.Model):
    """
    Logs non-webapp API requests by User
    """
    user = models.ForeignKey(
        'User',
        null=False,
        on_delete=models.CASCADE,
        help_text='The User account that made the request'
    )
    token = models.CharField(
        max_length=40,
        null=False,
        db_index=True,
        help_text='The API token used to make the request'
    )
    method = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        help_text='The HTTP verb used to make the request'
    )
    path = models.CharField(
        max_length=2083,
        null=False,
        help_text='The requested resource path'
    )
    response_code = models.IntegerField(
        null=True,
        help_text='The HTTP status code returned to the requester'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductType(models.Model):
    value = models.CharField(
        primary_key=True,
        max_length=50,
        null=False,
        blank=False,
        help_text='A suggested value for product type'
    )


class ProductionType(models.Model):
    value = models.CharField(
        primary_key=True,
        max_length=50,
        null=False,
        blank=False,
        help_text='A suggested value for production type'
    )
