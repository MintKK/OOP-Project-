/* Extra to include jQuery without source HTML */
/* var script = document.createElement('script');
script.src = 'vendor/jquery/jqery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script) */
 
$(document).ready(function() {

    // Dynamic Rows Code
    $("#add_row").on("click", function() {
        // Get max row id and set new id
        var newid = 0;
        $.each($("#tab_logic tr"), function() {
            if (parseInt($(this).data("id")) > newid) {
                newid = parseInt($(this).data("id"));
            }
        });
        
        newid++;
        
        var tr = $("<tr></tr>", {
            id: "addr"+newid,
            "data-id": newid
        });
        
        // loop through each td and create new elements with name of newid
        $.each($("#tab_logic tbody tr:nth(0) td"), function() {
            var cur_td = $(this);
            
            var children = cur_td.children();
            
            var td;
            // add new td and element if it has a name
            if ($(this).data("name") !== undefined) {
                td = $("<td></td>", {
                    "data-name": $(cur_td).data("name")
                });
                
                var c = $(cur_td).find($(children[0]).prop('tagName')).clone().val("");
                c.attr("name", $(cur_td).data("name") + newid);
                c.appendTo($(td));
                td.appendTo($(tr));
            } else {
                td = $("<td></td>", {
                    'text': $('#tab_logic tr').length
                }).appendTo($(tr));
            }
        });
        
        // add delete button and td
        /*
        $("<td></td>").append(
            $("<button class='btn btn-danger glyphicon glyphicon-remove row-remove'></button>")
                .click(function() {
                    $(this).closest("tr").remove();
                })
        ).appendTo($(tr));
        */
        
        // add the new row
        $(tr).appendTo($('#tab_logic'));
        
        $(tr).find("td button.row-remove").on("click", function() {
             $(this).closest("tr").remove();
        });
    });

    // Sortable Code
    var fixHelperModified = function(e, tr) {
        var $originals = tr.children();
        var $helper = tr.clone();
    
        $helper.children().each(function(index) {
            $(this).width($originals.eq(index).width())
        });
        
        return $helper;
    };
  
    $(".table-sortable tbody").sortable({
        helper: fixHelperModified      
    }).disableSelection();

    $(".table-sortable thead").disableSelection();
    
    /* Submit data */
    jsonStore = {};
    $("#submit_data").on("click", function() {
        
        editFormValidity = "True";
        function submitData() {
 
            $.confirm({
            title: 'Submit data',
            content: 'Confirm data submission? <b>(Once added, the new careers cannot be removed)</b>',
            buttons: {
                confirm: function () {
                    /* Iterate through all except 0 clone */    
                    $(".form-control:not([name='name0'], [name='salary0'], [name='desc0'])").each(function() {
                        
                        // Previous condition: if (!inputvalue.trim())
                        var inputvalue = $(this).val();
                        if (inputvalue == null || inputvalue === "") {
                            
                            editFormValidity = "False";
                            return;
                                // prompt("input " + $(this).attr("name") );
                        }
                        /* Send to JSON */
                        jsonStore[$(this).attr("name")] = $(this).val();
                           
                    });
                    
                    $("select").slice(1).each(function() {
                        
                        var inputvalue = $(this).val();
                        if (inputvalue == null || inputvalue === "") {
                            
                            editFormValidity = "False";
                            return;
                            
                        }
                        /* Send to JSON */    
                        jsonStore[$(this).attr("name")] = $(this).val();
                            
                    });

                    if (editFormValidity === "False") {
                        $.alert({
                                title: '',
                                content: '<span style="color: red; font-weight: bold;">Error:</span> Please fill out all inputs before submitting',
                        });
                        return;
                    }    
                    
                    localStorage.setItem('jsonStore', JSON.stringify(jsonStore));

                    console.log(jsonStore);


                    $.alert({
                        title: 'Data submitted',
                        content: '',
                        buttons: {
                            OK: function () {
                                location.reload();
                            }
                        }
                    });
                },
                cancel: function () {
                    $.alert('Canceled');
                } 
                /*,
                somethingElse: {
                    text: 'Something else',
                    btnClass: 'btn-blue',
                    keys: ['enter', 'shift'],
                    action: function(){
                        $.alert('Something else?');
                    }
                } */
            }
        });
    }
        submitData();  
    });
    /* Event triggers, once */
    $("#add_row").trigger("click"); 
   /* $("#submit_data").trigger("click"); */ /* Check if works */
    
});