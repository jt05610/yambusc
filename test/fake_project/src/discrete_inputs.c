#include "data_model/discrete_inputs.h"

/*
 * start get_user code
 */
None/*
 * end get_user code
 */

uint16_t
get_btn_forward()
{
/*
 * start get_btn_forward code
 */
    return 0;
/*
 * end get_btn_forward code
 */
}

uint16_t
get_btn_backward()
{
/*
 * start get_btn_backward code
 */
    return 0;
/*
 * end get_btn_backward code
 */
}

uint16_t
get_btn_inject()
{
/*
 * start get_btn_inject code
 */
    return 0;
/*
 * end get_btn_inject code
 */
}
 
static pt_read_t getters[N_DISCRETE_INPUTS] = { 
    get_btn_forward,
    get_btn_backward,
    get_btn_inject,
};


static primary_table_interface_t interface = {
        .read=getters,
        .write=0,
};

void
discrete_inputs_create(PrimaryTable base)
{
    base->vtable = &interface;
/*
 * start get_create code
 */
None/*
 * end get_create code
 */
}
