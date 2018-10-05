class QueryParameter:
    def __init__(self, name, par_type, description):
        self.name = name
        self.par_type = par_type
        self.description = description
    
    def getCourseParameters():
        result = []

        result.append(QueryParameter(
            'course_id',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'term',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'call_number',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'course_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'bulletin_flags',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'division_code',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'credit_amount',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'prefix_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'prefix_long_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'instructor_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'approval',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'school_code',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'school_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'campus_code',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'campus_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'type_code',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'type_name',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'num_enrolled',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'max_size',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'min_units',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'num_fixed_units',
            'Integer',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'class_notes',
            'String',
            'I am a valid description'
            ))
        result.append(QueryParameter(
            'meeting_times',
            'String',
            'I am a valid description'
            ))        

        return result




