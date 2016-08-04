var hourly = 1
var daily = 2
var result_count = 0;
var PAGE_STEP = 100;
var text_pattern = "";

function search_by_date() {
    text_pattern = "";
    var v_od = $("#datumOD").val();
    var v_do = $("#datumDO").val();
    var hourly_daily = get_hourly_daily();
    ajax_url = "./search?od="+v_od+"&do="+v_do;
    histogram_url = "./histogram?od="+v_od+"&do="+v_do+"&hd="+hourly_daily;
    search_ajax(ajax_url);

    $("#hist").attr("src",histogram_url);

}

function search_by_text() {

    var pattern = $("#textInput").val();
    var hourly_daily = get_hourly_daily();
    text_pattern = pattern;
    ajax_url = "./search?pattern="+pattern;
    histogram_url = "./histogram?pattern="+pattern+"&hd="+hourly_daily;
    search_ajax(ajax_url);

    $("#hist").attr("src",histogram_url);

}

// zpracovani vysledku a zavolani funkce zobrazujici vypis logu
function search_ajax(ajax_url) {
    $.ajax({
        url:ajax_url,
        success: function(result) {
            var s = "Bylo nalezeno "+result+" výsledků";
            result_count =  Number(result);
            $("#resultCountDiv").html(s);
            if (result_count>0) {
                show_page(0);
            } else {
                $("#resultTableDiv").html("");
                $("#resultPagerDiv").html("");
            }
        }
    });
}
// zobrazeni vypisu logu
function show_page(page_index) {
    ajax_url = "./show?offset="+page_index*PAGE_STEP;
    $.ajax({
        url:ajax_url,
        success: function(result) {
            var table = "<TABLE CELLSPACING=\"5\"><TR><TH>Jméno souboru</TH><TH>Datum</TH><TH>Metoda</TH><TH>Zpráva</TH></TR>"
            var logs = JSON.parse(result);
            if (text_pattern!="") {
                for (i=0;i<logs.length;i++) {
                    logs[i].message=logs[i].message.split(text_pattern).join("<B>"+text_pattern+"</B>");
                }
            }
            for (i=0;i<logs.length;i++) {
                table = table + "<TR><TD>"+logs[i].name+"</TD><TD>"+logs[i].date+"</TD><TD>"+logs[i].method+"</TD><TD>"+logs[i].message+"</TD></TR>";
            }

            table = table + "</TABLE>";
            $("#resultTableDiv").html(table);
            create_page_links(page_index);
        }
    });
}
// odkazy na strankovani logu
function create_page_links(page_index) {
    if (result_count<PAGE_STEP) {
        $("#resultPagerDiv").html("");
    } else {
        var output = "";
        for (i=0;result_count>(PAGE_STEP*i);i++) {
            var item = "" + (i+1);
            if (page_index!=i) {
                item = "<a href=\"javascript:show_page("+i+");\"> "+item+"</a>";
            }
            output = output + item + " ";
        }
        $("#resultPagerDiv").html(output);

    }


}





function get_hourly_daily() {
    if ($("#radioDaily").prop("checked"))
        return daily;
    else
        return hourly;

}