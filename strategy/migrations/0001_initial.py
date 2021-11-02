# Generated by Django 2.2 on 2021-11-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorpDataQuarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_name', models.CharField(max_length=20)),
                ('time_point', models.CharField(choices=[('201503', '201503'), ('201506', '201506'), ('201509', '201509'), ('201512', '201512'), ('201603', '201603'), ('201606', '201606'), ('201609', '201609'), ('201603', '201612'), ('201703', '201703'), ('201706', '201706'), ('201709', '201709'), ('201712', '201712'), ('201803', '201803'), ('201806', '201806'), ('201809', '201809'), ('201812', '201812'), ('201903', '201903'), ('201906', '201906'), ('201909', '201909'), ('201912', '201912'), ('202003', '202003'), ('202006', '202006'), ('202009', '202009'), ('202012', '202012'), ('202103', '202103'), ('202106', '202106')], max_length=6)),
                ('pbr', models.FloatField(blank=True, null=True)),
                ('per', models.FloatField(blank=True, null=True)),
                ('roe', models.FloatField(blank=True, null=True)),
                ('debt_ratio', models.FloatField(blank=True, null=True)),
                ('operating_margin', models.FloatField(blank=True, null=True)),
                ('borrowing_dependence', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CorpDataYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_name', models.CharField(max_length=20)),
                ('time_point', models.CharField(choices=[('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020')], max_length=4)),
                ('pbr', models.FloatField(blank=True, null=True)),
                ('per', models.FloatField(blank=True, null=True)),
                ('roe', models.FloatField(blank=True, null=True)),
                ('debt_ratio', models.FloatField(blank=True, null=True)),
                ('operating_margin', models.FloatField(blank=True, null=True)),
                ('borrowing_dependence', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]