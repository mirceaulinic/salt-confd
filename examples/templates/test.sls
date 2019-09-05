Hello world!

I'm running on {{ grains.osfullname }} {{ grains.osrelease }}, and I have the
following IPv6 addresses:

{%- for addr in grains.ipv6 %}
- {{ addr }}
{%- endfor %}
