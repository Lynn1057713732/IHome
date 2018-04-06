function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas', function (response) {
        if(response.errno == '0') {
            //渲染城区信息<option value="1">东城区</option>
            //遍历每一个城区
            $.each(response.data, function (i, area) {
                $('#area-id').append('<option value="' + area.aid + '">' + area.aname + '</option>');
            });
        }
        else{
            alert(response.errmsg);
        }
    })

    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();
        //准备参数
        var params = {};

        //收集房屋input标签数据
        //serializeArray()收集form表单中需要提交的input标签，收集到一个数组对象中
        // map 遍历对象，比如说数组对象
        // obj == {name: "title", value: "1"}
        $(this).serializeArray().map(function (obj) {
            params[obj.name] = obj.value;
        });

        //收集房屋的设施信息checkbox,不加这段那么显示的facility只有最后一个
        //  $(':checkbox:checked[name=facility]') == 收集界面上被选中的name为facility的checkbox
        // each 遍历界面上收集到的标签
        // elem == <input type="checkbox" name="facility" value="2">热水淋浴
        facilities = [];
        $(':checkbox:checked[name=facility]').each(function (i, elem) {
            // console.log(elem);
            facilities[i] = elem.value;
        });
        params['facility'] = facilities;

        //发送房屋数据给后端，ajax
        $.ajax({
            url:'/api/1.0/houses',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if(response.errno == '0'){

                }
                else if (response.errno == '4101') {
                    location.href = '/';
                }
                else{
                    alert(response.errmsg)
                }
            }
        })
    })
    // TODO: 处理图片表单的数据

})