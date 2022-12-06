#ifndef {{ project_name }}_{{ header_name }}_H
#define {{ project_name }}_{{ header_name }}_H

#include "data_model/primary_table.h"

#define N_{{ header_name }} {{ table_size }}

/*
 * Auto generated code: changes will be overwritten!
 */
{% for function in functions %}
{{ function }}
{% endfor %}
void {{ table_name }}_create(PrimaryTable base);

/*
 * End auto generated code.
 */

/*
 * User code: changes will be saved.
 */
{{ user_code }}
/*
 * End user code.
 */

#endif // {{ project_name }}_{{ header_name }}_H