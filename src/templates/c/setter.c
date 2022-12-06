uint16_t
set_{{ function_name }}(uint16_t value)
{
/*
 * start set_{{ function_name }} code
 */
{% if user_code %}{{ user_code }}{% else %}    return 0;
{% endif %}/*
 * end set_{{ function_name }} code
 */
}
