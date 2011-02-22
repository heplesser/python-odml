#-*- coding: utf-8
from value import Value

class Property(object):
    """An odML Property"""
    def __init__(self, name, value, section=None, 
        synonym=None, definition=None, dependency=None, dependencyValue=None, mapping=None,
        unit=None, dtype=None, uncertainty=None):
    	"""
    	create a new Property
    	
    	*value*
    	    specifies a direct value that shall be assigned as a first value
    	    if *value* is a list, the whole list of values will be assigned.
    	    Further info
    	    
	    	*unit*
	            the unit of the value(s)
	
	        *dtype*
	            the data type of the value(s)
	
	        *uncertainty*
	            an estimation of uncertainty of the value(s)

    	*section*
    	    the parent section to which this property belongs
    	
    	
	 * @param definition {@link String}
	 * @param dependency {@link String}
	 * @param dependencyValue {@link String}
	 * @param mapping {@link URL}
    	"""
        #TODO doc description for arguments
        #TODO validate arguments
        self._name = name
        self._section = section
        self._values = []

        if type(value) is list:
            for v in value:
                if not isinstance(v, Value):
                    v = Value(v, unit=unit, uncertainty=uncertainty, dtype=dtype)
                self.add_value(v)
        elif not value is None:
            self.add_value(value)

        # getter and setter methods are omnitted for now, but they can easily
        # be introduced later using python-properties

    #odML "native" properties
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value

    def __repr__(self):
        return "<Property %s>" % self._name



    # API (public) 
    #
    #  properties
    @property
    def values(self):
        """returns the list of values for this property"""
        return self._values
        
    @property
    def value(self):
        """
        returns the value of this property (or list if multiple values are present)
        
        use :ref:`values`() to always return the list"""
        if len(self._values) == 1:
            return self._values[0]
        
        #create a copy of the list, so mutations in there won’t affect us:
        return self._values[:] 
    
    def add_value(self, value, unit=None, dtype=None, uncertainty=None, copy_attributes=False):
        """
        adds a value to the list of values
        
        If *value* is not an odml.Value instance, such an instance will be created
        given the addition function arguments (see :ref:`__init__` for their description).
        
        If *value* is not an odml.Value instance and *unit*, *dtype* or *uncertainty* are
        missing, the values will be copied from the last value in this properties
        value-list if *copy_attributes* is True. If there is no value present to be
        copied from, an IndexError will be raised.
        """
        if not isinstance(value, Value):
            if copy_attributes:
                if unit is None: unit = self._values[-1].unit
                if type is None: dtype = self._values[-1].dtype
                if uncertainty is None: uncertainty = self._values[-1].uncertainty
            val = Value(value, unit=unit, dtype=dtype, uncertainty=uncertainty)
        self._values.append(value)
        value._property = self

    def __iter__(self):
        return self._values.__iter__()
    # API (private)
    #def _fire_change_event(self, prop_name): #TODO see how we handle events
    #    return None #FIXME: IMPLEMENT