#include "data_model/{{ table_name }}.h"

/*
 * start get_user code
 */
{{ user_header_code }}/*
 * end get_user code
 */
{% for function in functions %}
{{ function }}
{% endfor %} {% for array in arrays %}
{{ array }}
{% endfor %}

{{ interface }}

void
{{ table_name }}_create(PrimaryTable base)
{
    base->vtable = &interface;
/*
 * start get_create code
 */
{{ create_code }}/*
 * end get_create code
 */
}

