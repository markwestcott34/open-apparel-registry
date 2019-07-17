# Generated by Django 2.0.13 on 2019-07-03 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_add_fields_to_facility_claim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityclaim',
            name='company_name',
            field=models.CharField(blank=True, help_text='The company name for the facility', max_length=200, verbose_name='company name'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='contact_person',
            field=models.CharField(help_text='The contact person for the facility claim', max_length=200, verbose_name='contact person'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='email',
            field=models.EmailField(help_text='The contact email for the facility claim', max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_address',
            field=models.CharField(blank=True, help_text='The editable facility address for this claim.', max_length=200, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_average_lead_time',
            field=models.CharField(blank=True, help_text='The editable facilty avg lead time for this claim.', max_length=200, null=True, verbose_name='average lead time'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_description',
            field=models.TextField(blank=True, help_text='A description of the facility', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_minimum_order_quantity',
            field=models.CharField(blank=True, help_text='The editable facility min order quantity for this claim.', max_length=200, null=True, verbose_name='minimum order quantity'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_phone_number',
            field=models.CharField(blank=True, help_text='The editable facility phone number for this claim.', max_length=200, null=True, verbose_name='facility phone number'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_phone_number_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the editable facility phone number publicly visible?', verbose_name='is facility phone number publicly visible'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='facility_website',
            field=models.URLField(blank=True, help_text='The editable facility website for this claim.', null=True, verbose_name='facility website'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='office_address',
            field=models.CharField(blank=True, help_text='The editable office address for this claim.', max_length=200, null=True, verbose_name='office address'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='office_country_code',
            field=models.CharField(blank=True, choices=[('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Côte d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curacao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('XK', 'Kosovo'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MK', 'North Macedonia'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe,Sao Tome And Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Vietnam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], help_text='The editable office country code for this claim.', max_length=2, null=True, verbose_name='office country code'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='office_info_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the office info publicly visible?', verbose_name='is office publicly visible'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='office_official_name',
            field=models.CharField(blank=True, help_text='The editable office name for this claim.', max_length=200, null=True, verbose_name='office official name'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='office_phone_number',
            field=models.CharField(blank=True, help_text='The editable office phone number for this claim.', max_length=200, null=True, verbose_name='office phone number'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='parent_company',
            field=models.ForeignKey(default=None, help_text='The parent company of this facility claim.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='parent_company', to='api.Contributor', verbose_name='parent company'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='phone_number',
            field=models.CharField(help_text='The contact phone number for the facility claim', max_length=200, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='point_of_contact_email',
            field=models.EmailField(blank=True, help_text='The editable point of contact email', max_length=254, null=True, verbose_name='contact email'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='point_of_contact_person_name',
            field=models.CharField(blank=True, help_text='The editable point of contact person name', max_length=200, null=True, verbose_name='contact person'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='point_of_contact_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the point of contact info publicly visible?', verbose_name='is contact visible'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='preferred_contact_method',
            field=models.CharField(choices=[('EMAIL', 'EMAIL'), ('PHONE', 'PHONE')], help_text='The preferred contact method: email or phone', max_length=200, verbose_name='preferred contact method'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('DENIED', 'DENIED'), ('REVOKED', 'REVOKED')], default='PENDING', help_text='The current status of this facility claim', max_length=200, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='status_change_by',
            field=models.ForeignKey(help_text='The user who changed the status of this facility claim', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approver_of_claim', to=settings.AUTH_USER_MODEL, verbose_name='status changed by'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='status_change_date',
            field=models.DateTimeField(null=True, verbose_name='status change date'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='status_change_reason',
            field=models.TextField(blank=True, help_text='The reason entered when changing the status of this claim.', null=True, verbose_name='status change reason'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='verification_method',
            field=models.TextField(blank=True, help_text='An explanation of how the facility can be verified', verbose_name='verification method'),
        ),
        migrations.AlterField(
            model_name='facilityclaim',
            name='website',
            field=models.CharField(blank=True, help_text='The website for the facility', max_length=200, verbose_name='website'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='company_name',
            field=models.CharField(blank=True, help_text='The company name for the facility', max_length=200, verbose_name='company name'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='contact_person',
            field=models.CharField(help_text='The contact person for the facility claim', max_length=200, verbose_name='contact person'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='email',
            field=models.EmailField(help_text='The contact email for the facility claim', max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_address',
            field=models.CharField(blank=True, help_text='The editable facility address for this claim.', max_length=200, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_average_lead_time',
            field=models.CharField(blank=True, help_text='The editable facilty avg lead time for this claim.', max_length=200, null=True, verbose_name='average lead time'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_description',
            field=models.TextField(blank=True, help_text='A description of the facility', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_minimum_order_quantity',
            field=models.CharField(blank=True, help_text='The editable facility min order quantity for this claim.', max_length=200, null=True, verbose_name='minimum order quantity'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_phone_number',
            field=models.CharField(blank=True, help_text='The editable facility phone number for this claim.', max_length=200, null=True, verbose_name='facility phone number'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_phone_number_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the editable facility phone number publicly visible?', verbose_name='is facility phone number publicly visible'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='facility_website',
            field=models.URLField(blank=True, help_text='The editable facility website for this claim.', null=True, verbose_name='facility website'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='office_address',
            field=models.CharField(blank=True, help_text='The editable office address for this claim.', max_length=200, null=True, verbose_name='office address'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='office_country_code',
            field=models.CharField(blank=True, choices=[('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Côte d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curacao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('XK', 'Kosovo'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MK', 'North Macedonia'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe,Sao Tome And Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Vietnam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], help_text='The editable office country code for this claim.', max_length=2, null=True, verbose_name='office country code'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='office_info_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the office info publicly visible?', verbose_name='is office publicly visible'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='office_official_name',
            field=models.CharField(blank=True, help_text='The editable office name for this claim.', max_length=200, null=True, verbose_name='office official name'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='office_phone_number',
            field=models.CharField(blank=True, help_text='The editable office phone number for this claim.', max_length=200, null=True, verbose_name='office phone number'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='parent_company',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, help_text='The parent company of this facility claim.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.Contributor', verbose_name='parent company'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='phone_number',
            field=models.CharField(help_text='The contact phone number for the facility claim', max_length=200, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='point_of_contact_email',
            field=models.EmailField(blank=True, help_text='The editable point of contact email', max_length=254, null=True, verbose_name='contact email'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='point_of_contact_person_name',
            field=models.CharField(blank=True, help_text='The editable point of contact person name', max_length=200, null=True, verbose_name='contact person'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='point_of_contact_publicly_visible',
            field=models.BooleanField(default=False, help_text='Is the point of contact info publicly visible?', verbose_name='is contact visible'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='preferred_contact_method',
            field=models.CharField(choices=[('EMAIL', 'EMAIL'), ('PHONE', 'PHONE')], help_text='The preferred contact method: email or phone', max_length=200, verbose_name='preferred contact method'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('DENIED', 'DENIED'), ('REVOKED', 'REVOKED')], default='PENDING', help_text='The current status of this facility claim', max_length=200, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='status_change_by',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The user who changed the status of this facility claim', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='status changed by'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='status_change_date',
            field=models.DateTimeField(null=True, verbose_name='status change date'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='status_change_reason',
            field=models.TextField(blank=True, help_text='The reason entered when changing the status of this claim.', null=True, verbose_name='status change reason'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='verification_method',
            field=models.TextField(blank=True, help_text='An explanation of how the facility can be verified', verbose_name='verification method'),
        ),
        migrations.AlterField(
            model_name='historicalfacilityclaim',
            name='website',
            field=models.CharField(blank=True, help_text='The website for the facility', max_length=200, verbose_name='website'),
        ),
    ]
