static pt_{{ access_type }}_t {{ array_name }}[{{ table_n_macro }}] = { {% for name in names %}
    {{ array_name[:3] }}_{{ name }},{% endfor %}
};