{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ module }}.{{ objname }}
   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

.. autoclass:: {{ module }}.{{ objname }}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
