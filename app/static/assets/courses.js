var count = 0
function addField() {
    var code = '<div><br><br>\
                                <div class="col-sm-2">\
                                    <select class="form-control selectionQuery" id="inputParameter" value="course_name">\
                                        <option value="course_id">course_id</option>\
                                        <option value="term">term</option>\
                                        <option value="call_number">call_number</option>\                                        <option value="course_name" selected="selected">course_name</option>\
                                        <option value="bulletin_flags">bulletin_flags</option>\
                                        <option value="division_code">division_code</option>\
                                        <option value="credit_amount">credit_amount</option>\
                                        <option value="prefix_name">prefix_name</option>\
                                        <option value="prefix_long_name">prefix_long_name</option>\
                                        <option value="instructor_name">instructor_name</option>\
                                        <option value="approval">approval</option>\
                                        <option value="school_code">school_code</option>\
                                        <option value="school_name">school_name</option>\                                        <option value="campus_code">campus_code</option>\
                                        <option value="campus_name">campus_name</option>\
                                        <option value="type_code">type_code</option>\
                                        <option value="type_name">type_name</option>\
                                        <option value="num_enrolled">num_enrolled</option>\
                                        <option value="max_size">max_size</option>\
                                        <option value="min_units">min_units</option>\
                                        <option value="num_fixed_units">num_fixed_units</option>\
                                        <option value="class_notes">class_notes</option>\
                                        <option value="meeting_times">meeting_times</option>\
                                    </select>\
                                </div>' +
        '<div class="col-sm-9">\
                                    <input class="form-control" id="inputParameterValue" type="text" value="DATA%20STRUCTURES%20IN%20JAVA">\
                                </div>' +
        '<div class="col-sm-1">\
                                    <button type="button" class="btn btn-warning deletion" onclick="deleteField(this)">X</button>\
                                </div>\
                            </div>'
    //<div id = "' + count+1 + '"></div>'
    document.getElementById("fieldToAdd").innerHTML += code
    //document.getElementById(count.toString()).innerHTML += code
    //count++
}

function deleteField(button) {
    $(button).parent().parent().remove();
}

function queryFunction(endpoint) {

    var req = endpoint + "Request";
    var resp = endpoint + "ResponseBlock";

    var apiCall = new XMLHttpRequest();
    apiCall.onreadystatechange = function () {
        document.getElementById(req).innerHTML = apiRequest;
        if (apiCall.readyState == XMLHttpRequest.DONE && this.status == 200) {
            var obj = JSON.parse(apiCall.responseText)
            var temp_text = "{\
                                            &quot;status_code&quot;: " + obj.status + ",\
                                            &quot;data&quot;: [\
                                            { \
                                                &quot;approval&quot;: &quot;&quot;,\
                                                &quot;bulletin_flags&quot;: &quot;CEFKGRUXI&quot;,\
                                                &quot;call_number&quot;: 68108,\
                                                &quot;campus_code&quot;: &quot;MORN&quot;,\
                                                &quot;campus_name&quot;: &quot;MORNINGSIDE&quot;,\
                                                &quot;class_notes&quot;: &quot;&quot;,\
                                                &quot;course_id&quot;: &quot;COMS3134S001&quot;,\
                                                &quot;course_name&quot;: &quot;DATA STRUCTURES IN JAVA&quot;,\
                                                &quot;credit_amount&quot;: &quot;null&quot;,\
                                                &quot;division_code&quot;: &quot;SS&quot;,\
                                                &quot;instructor_name&quot;: &quot;BLAER, PAUL &quot;,\
                                                &quot;max_size&quot;: 999,\
                                                &quot;meeting_times&quot;: &quot;null&quot;,\
                                                &quot;min_units&quot;: 0,\
                                                &quot;num_enrolled&quot;: 68,\
                                                &quot;num_fixed_units&quot;: 30,\
                                                &quot;prefix_long_name&quot;: &quot;COMPUTER SCIENCE&quot;,\
                                                &quot;prefix_name&quot;: &quot;COMPUT SCI&quot;,\
                                                &quot;school_code&quot;: &quot;SPEC&quot;,\
                                                &quot;school_name&quot;: &quot;SCHOOL OF PROFESSIONAL STUDIES&quot;,\
                                                &quot;term&quot;: &quot;20182&quot;,\
                                                &quot;type_code&quot;: &quot;LC&quot;,\
                                                &quot;type_name&quot;: &quot;LECTURE&quot;\
                                            }\
                                        ],\
                                        &quot;status_txt&quot;: &quot;OK&quot;\
                                    }"
            document.getElementById(resp).innerHTML = temp_text;
            document.getElementById(resp).style.color = "green";
        } else {
            var responseObj = JSON.parse(this.response);
            document.getElementById(resp).innerHTML = "ERROR " + this.status + ": " + responseObj.message;
            document.getElementById(resp).style.color = "red";
        }
    }
    if (endpoint == "select") {
        apiRequest = "http://127.0.0.1:5000/api/courses/select?course_id="
            + document.getElementById("inputCourseID").value
            + "&term="
            + document.getElementById("inputTerm").value
            + "&key="
            + document.getElementById("inputKey1").value;
    }
    else if (endpoint == "search") {
        apiRequest = "http://127.0.0.1:5000/api/courses/search?"
            + document.getElementById("inputParameter").value
            + "="
            + document.getElementById("inputParameterValue").value
            + "&key="
            + document.getElementById("inputKey2").value;
    }
    apiCall.open("GET", apiRequest);
    apiCall.send();
}