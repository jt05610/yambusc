static data_model_t data_model[{{ n_tables }}] = { {% for table in tables %}
    {{table}},{% endfor %}
};