function get_history()
{
document.getElementById('com').innerHTML="<textarea id='history' class='ta' rows='10' cols='90'></textarea>";
$.ajax({
            type: "GET",
            url:"/history/",
            dataType: "json",
            contentType: "application/json",
            success: function (data)
            {
                for(i=0;i<data.length;i++)

                {
                console.log(data[i].command)
                 <!--$(data[i].command).appendTo('#history')-->
                 document.getElementById("history").value += i+1+"."
                 document.getElementById("history").value += data[i].command+"\n"
                 <!--var myLineBreak = history.replace(/\r\n|\r|\n/g,"\n");-->


                }
                 <!--Clear exiting data here-->
                 <!--$('#history')-->
                    <!--.remove()-->
                    <!--.end()-->
                <!--$.each(data.command,function(i,obj)-->
                <!--{-->
                <!--console.log(obj)-->
                <!--var div_data=obj.username;-->
                <!--var div_name=obj.command;-->
                <!--console.log(div_data)-->
                $(data[0].username).appendTo('#history');
                <!--});-->

                }
          });



}

function get_Add()
{
acount=acount+1;
document.getElementById('Ademo').innerHTML="<select id='Aselect2'></select>";

$.ajax({
            type: "GET",
            url:"/appliance/",
            dataType: "json",
            success: function (data) {
                console.log(data)
                 <!--Clear exiting data here-->
                 $('#Aselect2')
                    .find('option')
                    .remove()
                    .end()
                $.each(data.data,function(i,obj)
                {
                <!--console.log(obj)-->
                var div_data="<option value="+obj+">"+obj+"</option>";
                $(div_data).appendTo('#Aselect2');
                });
                }
          });


}

function get_Hdd()
{
hcount=hcount+1;
document.getElementById('Hdemo').innerHTML="<select id='Hselect2'></select>";

$.ajax({
            type: "GET",
            url:"/host/",
            dataType: "json",
            success: function (data) {
                console.log(data)
                 <!--Clear exiting data here-->
                 $('#Hselect2')
                    .find('option')
                    .remove()
                    .end()
                $.each(data.data,function(i,obj)
                {
                <!--console.log(obj)-->
                var div_data="<option value="+obj+">"+obj+"</option>";
                $(div_data).appendTo('#Hselect2');
                });
                }
          });


}


function get_options()
{

    var host=document.getElementById('Hselect').value;
    var testcases=document.getElementById('Tselect').value;
    var app=document.getElementById('Aselect').value;


    $(document).ready(function(){
        function getCookie(c_name) {
            if(document.cookie.length > 0) {
                c_start = document.cookie.indexOf(c_name + "=");
                if(c_start != -1) {
                    c_start = c_start + c_name.length + 1;
                    c_end = document.cookie.indexOf(";", c_start);
                    if(c_end == -1) c_end = document.cookie.length;
                    return unescape(document.cookie.substring(c_start,c_end));
                }
            }
            return "";
        }

        $(function () {
            $.ajaxSetup({
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });
        });
    });
    if(hcount==0 && acount==0)
    {
    var myEvent = {'host': host, 'test': testcases, 'app': app}
     $.ajax( {

                    type: "POST",
                    url: "/getoptions/",

                    data: JSON.stringify(myEvent),
                    contentType: "application/json; charset=utf-8",
                    crossDomain: true, // enable this
                    dataType: "json",
                    success: function (returnObject) { //msg.Data.TransactionList
                        // Do whatever you want to do
                        console.log(returnObject['session_id'])
                        load_execution_log(returnObject['session_id'], 0)
                    }

              });

    }

    else if(acount==0 && hcount==1)
    {


    var hdd=document.getElementById('Hselect2').value;
    var myevent2={'host': host, 'test': testcases, 'app': app,'host2':hdd}
    $.ajax( {

                    type: "POST",
                    url: "/getoptions/",

                    data: JSON.stringify(myevent2),
                    contentType: "application/json; charset=utf-8",
                    crossDomain: true, // enable this
                    dataType: "json",
                    success: function (returnObject) { //msg.Data.TransactionList
                        // Do whatever you want to do
                       console.log(returnObject['session_id'])
                       load_execution_log(returnObject['session_id'], 0)
                    }

              });

    }


    else if(acount==1 && hcount==0)
    {
    var add=document.getElementById('Aselect2').value;
    var myEvent1 = {'host': host, 'test': testcases, 'app': app,'app1':add}


     $.ajax( {

                    type: "POST",
                    url: "/getoptions/",

                    data: JSON.stringify(myEvent1),
                    contentType: "application/json; charset=utf-8",
                    crossDomain: true, // enable this
                    dataType: "json",
                    success: function (returnObject) { //msg.Data.TransactionList
                        // Do whatever you want to do
                        console.log(returnObject['session_id'])
                        load_execution_log(returnObject['session_id'], 0)
                    }

              });

    }

    else
    {
    var add=document.getElementById('Aselect2').value;
    var hdd=document.getElementById('Hselect2').value;
    var myevent3={'host': host, 'test': testcases, 'app': app,'host2':hdd,'app2':add}
    $.ajax( {

                    type: "POST",
                    url: "/getoptions/",

                    data: JSON.stringify(myevent3),
                    contentType: "application/json; charset=utf-8",
                    crossDomain: true, // enable this
                    dataType: "json",
                    success: function (returnObject) {
                        //msg.Data.TransactionList
                        // Do whatever you want to do
                        console.log(returnObject['session_id'])
                        load_execution_log(returnObject['session_id'], 0)


                    }

              });


    }

}

var hcount=0,acount=0;
function get_details()
{


  $.ajax({
            type: "GET",
            url:"/host/",
            dataType: "json",
            success: function (data) {
                console.log(data)
                 <!--Clear exiting data here-->
                 $('#Hselect')
                    .find('option')
                    .remove()
                    .end()
                $.each(data.data,function(i,obj)
                {
                <!--console.log(obj)-->
                var div_data="<option value="+obj+">"+obj+"</option>";
                $(div_data).appendTo('#Hselect');
                });
                }
          });



$.ajax({
            type: "GET",
            url:"/testcases/",
            dataType: "json",
            success: function (data) {
                console.log(data)
                 <!--Clear exiting data here-->
                 $('#Tselect')
                    .find('option')
                    .remove()
                    .end()
                $.each(data.data,function(i,obj)
                {
                <!--console.log(obj)-->
                var div_data="<option value="+obj+">"+obj+"</option>";
                $(div_data).appendTo('#Tselect');
                });
                }
          });


$.ajax({
            type: "GET",
            url:"/appliance/",
            dataType: "json",
            success: function (data) {
                console.log(data)
                 <!--Clear exiting data here-->
                 $('#Aselect')
                    .find('option')
                    .remove()
                    .end()
                $.each(data.data,function(i,obj)
                {
                <!--console.log(obj)-->
                var div_data="<option value="+obj+">"+obj+"</option>";
                $(div_data).appendTo('#Aselect');
                });
                }
          });
}

function get_timestamp() {
    if (!Date.now) {
    Date.now = function() { return new Date().getTime(); }
    }
    else {
    return Date.now()
    }
}

function get_execution_log(exe_session_id, counter) {
    var counter = counter || 0;

    $(document).ready(function(){
        function getCookie(c_name) {
            if(document.cookie.length > 0) {
                c_start = document.cookie.indexOf(c_name + "=");
                if(c_start != -1) {
                    c_start = c_start + c_name.length + 1;
                    c_end = document.cookie.indexOf(";", c_start);
                    if(c_end == -1) c_end = document.cookie.length;
                    return unescape(document.cookie.substring(c_start,c_end));
                }
            }
            return "";
        }

        $(function () {
            $.ajaxSetup({
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });
        });
        });


    $.ajax({
            type: "POST",
            url:"/execution",
            headers: {"sessionid": exe_session_id, "count": counter},
            contentType: "application/json",
            success: function(data) {
            setTimeout(function()
            {
                <!--console.log("counter:" + counter)-->
                if (counter < data.count) {
                    for(i=0;i<data.result.length;i++) {
                        document.getElementById("exe_session").value += data.result[i];
                        document.getElementById("exe_session").value += "\n";
                        }
                    counter = data.count;
                    document.getElementById('exe_session').value += get_timestamp();
                    <!--console.log("data_counter:" + counter)-->
                }
                get_execution_log(exe_session_id, counter);
            }, 10000);
            },
            error: function() { alert("Some error occurred while fetching execution log for session " + exe_session_id + " ")}

            });
}

async function load_execution_log(exe_session_id, counter) {
    await get_execution_log(exe_session_id, counter);
}
