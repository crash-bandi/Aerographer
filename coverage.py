import xml.etree.ElementTree as ET

colors = {
    0: 'red',
    40: 'orange',
    60: 'yellow',
    80: 'yellowgreen',
    90: 'green'
}

coverage = int(float(ET.parse("coverage.xml").getroot().attrib["line-rate"]) * 100)

color = 'red'
if 60 > coverage >= 40:
    color = 'orange'
elif 80 > coverage >= 60:
    color = 'yellow'
elif 90 > coverage >= 80:
    color = 'yellowgreen'
elif coverage >= 90:
    color = 'green'

print(f'coverage-{coverage}%25-{color}')