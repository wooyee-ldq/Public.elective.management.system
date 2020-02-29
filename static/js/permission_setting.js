$(document).ready(function(){

    // 反选按钮点击事件
    $("#reverse_all").click(function(){
        $("#permission :checkbox").each(function(i){
            $(this).prop("checked", !$(this).prop("checked"));
        });
    });

    // 全选按钮点击事件
    $("#check_all").click(function(){
        $("#permission :checkbox").prop("checked", true);
    });

    // 同意按钮点击事件
    $("#agree").click(function(){
        var cid_arr = new Array();
        $("#permission input:checkbox[name='cid']:checked").each(function(i){
            cid_arr[i] = $(this).val()
        });
        if(cid_arr.length <= 0){
            alert("请先选择记录！")
        }else{
            $.ajax({
                url: "/admin/permissionAgree",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid_arr": cid_arr.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        for(let i = 0; i < cid_arr.length; i++) {
                            $("li span[cid='" + cid_arr[i] + "']").html("有权限")
                            $("#permission :checkbox").prop("checked", false)
                        }
                    }
                },
                error: function () {
                    alert("授权操作失败！")
                }
            })
        }

    });

    // 拒绝按钮点击事件
    $("#refuse").click(function(){
        var cid_arr = new Array();
        $("#permission input:checkbox[name='cid']:checked").each(function(i){
            cid_arr[i] = $(this).val()
        });
        if(cid_arr.length <= 0){
            alert("请先选择记录！")
        }else{
            $.ajax({
                url: "/admin/permissionRefuse",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid_arr": cid_arr.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        for(let i = 0; i < cid_arr.length; i++) {
                            $("li span[cid='" + cid_arr[i] + "']").html("无权限")
                            $("#permission :checkbox").prop("checked", false)
                        }
                    }
                },
                error: function () {
                    alert("撤销权限操作失败！")
                }
            })
        }

    });

})