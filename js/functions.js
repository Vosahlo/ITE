var hourly = 1
var daily = 2


function search_by_date() {

    var v_od = $("#datumOD").val();
    var v_do = $("#datumDO").val();
    var hourly_daily = get_hourly_daily();

    ajax_url = "./search?od="+v_od+"&do="+v_do;
    histogram_url = "./histogram?od="+v_od+"&do="+v_do+"&hd="+hourly_daily;
    $.ajax({
        url:ajax_url,
        success: function(result) {
            console.log(result)
        }
    });
    $("#hist").attr("src",histogram_url);

};

function search_by_text() {

    var pattern = $("#textInput").val();
    var hourly_daily = get_hourly_daily();
    ajax_url = "./search?pattern="+pattern;
    histogram_url = "./histogram?pattern="+pattern+"&hd="+hourly_daily;
    $.ajax({
        url:ajax_url,
        success: function(result) {
            console.log(result)
        }
    });
    $("#hist").attr("src",histogram_url);

};

function get_hourly_daily() {
    if ($("#radioDaily").prop("checked"))
        return daily;
    else
        return hourly;

}