# corndog
multicorn wrapper for datadog

# Install (essentials)
```bash
sudo apt-get install python-dev pgxnclient
sudo pgxn install multicorn
git clone https://github.com/globalundo/corndog
cd corndog
python setup.py install
```

# Install from scratch on debian jessie
```bash
# Add postgresql.ord repo
# https://wiki.postgresql.org/wiki/Apt
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6 postgresql-server-dev-9.6
sudo apt-get install python-dev pgxnclient
sudo apt-get install git
git clone https://github.com/globalundo/corndog
cd corndog
python setup.py install
#sudo sed -i 's/local   all             postgres                                peer/local   all             all                                trust/g' /etc/postgresql/9.6/main/pg_hba.conf
#sudo sed -i "s/#listen_addresses.*/listen_addresses = '*'/g" /etc/postgresql/9.6/main/postgresql.conf
#sudo sed -i 's|host.*|host all all 127.0.0.1/32 trust|g' /etc/postgresql/9.6/main/pg_hba.confsudo service postgresql restart
#psql -U postgres <<EOF
#CREATE DATABASE datadog;
#\c datadog
#CREATE EXTENSION multicorn;
#CREATE SERVER corndog FOREIGN DATA WRAPPER multicorn
#options (
#  wrapper 'corndog.DatadogForeignDataWrapper',
#  api_key 'YOUR_API_KEY_HERE',
#  app_key 'YOUR_APP_KEY_HERE'
#);
#CREATE FOREIGN TABLE metrics (
#    timestamp float,
#    value float,
#    startdate int,
#    enddate int,
#    query text,
#    scope text
#) server corndog ;
#select * from metrics limit 1;
#select * from metrics where query='system.cpu.user{*}' limit 1;
#select timestamp, value from metrics where query='system.cpu.user{*}' and startdate = extract(epoch from (now()-'20 days'::interval))::int;
#select timestamp, value from metrics where query='system.cpu.user{*}' and startdate = extract(epoch from (now()-'12 hours'::interval))::int and enddate = extract(epoch from (now()-'2 hours'::interval))::int;
#
#EOF

```

# Usage
```sql
CREATE EXTENSION multicorn;
CREATE SERVER corndog FOREIGN DATA WRAPPER multicorn
options (
  wrapper 'corndog.DatadogForeignDataWrapper',
  api_key 'YOUR_API_KEY_HERE',
  app_key 'YOUR_APP_KEY_HERE'
);
CREATE FOREIGN TABLE metrics (
    timestamp float,
    value float,
    startdate int,
    enddate int,
    query text,
    scope text
) server corndog;
select * from metrics limit 1;
select * from metrics where query='system.cpu.user{*}' limit 1;
select timestamp, value from metrics where query='system.cpu.user{*}' and startdate = extract(epoch from (now()-'20 days'::interval))::int;
select timestamp, value from metrics where query='system.cpu.user{*}' and startdate = extract(epoch from (now()-'12 hours'::interval))::int and enddate = extract(epoch from (now()-'2 hours'::interval))::int;
```
