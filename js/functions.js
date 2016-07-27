function search_by_date() {

    var v_od = $("#datumOD").val();
    var v_do = $("#datumDO").val();
    console.log(" "+v_od+" "+v_do);
    ajax_url = "./search?od="+v_od+"&do="+v_do;
    histogram_url = "./histogram?od="+v_od+"&do="+v_do;
    /*
    $.ajax({
        url:ajax_url,
        success: function(result) {
            console.log(result)
        }
    });
    */
    $("#pict").attr("src",histogram_url);

};