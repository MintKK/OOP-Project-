/* Extra to include jQuery without source HTML */
/* var script = document.createElement('script');
script.src = 'vendor/jquery/jqery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script) */

 $(document).ready(function(){
     
     // Load added jobs
     function loadNewJobs() {
         
        var jsonStore = JSON.parse(localStorage.getItem("jsonStore"));  // Remember to parse to JSON object

        if ($.isEmptyObject(jsonStore)) {
            return;
        }
        // Console checking
        console.log(jsonStore);
        console.log(Object.keys(jsonStore).length);

        for (var i = 1; i < (Object.keys(jsonStore).length / 4 + 1); i++) {
            var Row = $(document.createElement("tr"));
            var Name = jsonStore[("name" + i)];
            var Range = jsonStore[("range" + i)];
            var Tags = jsonStore[("desc" + i)];
            var Industry;
            if (jsonStore[("sel" + i)] == "1") {
                Industry = "Primary Industry" ;
            }
            else if (jsonStore[("sel" + i)] == "2") {
                Industry = "Secondary Industry" ;
            }
            else if (jsonStore[("sel" + i)] == "3") {
                Industry = "Tertiary Industry" ;
            }
            else if (jsonStore[("sel" + i)] == "4") {
                Industry = "Quaternary Industry" ;
            }
            else if (jsonStore[("sel" + i)] == "5") {
                Industry = "Unspecified" ;    
            }

            $(Row).html("<td>" + Name + "</td><td>" + Range + "</td><td>" + Tags + "</td><td>" + Industry + "</td>" + "<td><a href='startbootstrap-portfolio-item-gh-pages/demoEdit.html' class='btn btn-warning job-link'><span class='fa fa-link'></span></a></td>");

            $('#tab_logic > tbody:last-child').append(Row);
        }
     }
     
     loadNewJobs();
     
    // Code for filter  
    $('.filterable .btn-filter').click(function(){
        var $panel = $(this).parents('.filterable'),
        $filters = $panel.find('.filters input'),
        $tbody = $panel.find('.table tbody');
        if ($filters.prop('disabled') === true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    $('.filterable .filters input').keyup(function(e){
        // Ignore tab key 
        var code = e.keyCode || e.which;
        if (code == '9') return;
        // Useful DOM data and selectors
        var $input = $(this),
        inputContent = $input.val().toLowerCase(),
        $panel = $input.parents('.filterable'),
        column = $panel.find('.filters th').index($input.parents('th')),
        $table = $panel.find('.table'),
        $rows = $table.find('tbody tr');
        // Dirtiest filter function ever ;) 
        var $filteredRows = $rows.filter(function(){
            var value = $(this).find('td').eq(column).text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        // Clean previous no-result if exist 
        $table.find('tbody .no-result').remove();
        // Show all rows, hide filtered ones (never do that outside of a demo ! xD) 
        $rows.show();
        $filteredRows.hide();
        // Prepend no-result row if all rows are filtered 
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
        }
    });
    /* Event triggers, once */
    /* $("#add_row").trigger("click"); */
   /* $("#submit_data").trigger("click"); */ /* Check if works */
    
});