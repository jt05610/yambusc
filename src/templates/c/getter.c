uint16_t
get_{{ function_name }}()
{
/*
 * start get_{{ function_name }} code
 */
{% if user_code %}{{ user_code }}{% else %}    return 0;
{% endif %}/*
 * end get_{{ function_name }} code
 */
}