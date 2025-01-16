//****************针对第一种方式的具体js实现部分******************//
//****************所使用的数据是city.js******************//
var btn = document.getElementsByClassName('met1')[0];
var addrShow = document.getElementById('addr-show');
var prov = document.getElementById('prov');
var city = document.getElementById('city');
var country = document.getElementById('country');

/*用于保存当前所选的省市区*/
var current = {
    prov: '',
    city: '',
    country: ''
};

/*自动加载省份列表*/
(function showProv() {
    btn.disabled = true;
    var len = province.length;
    for (var i = 0; i < len; i++) {
        var provOpt = document.createElement('option');
        provOpt.value = provOpt.innerText = province[i]['name'];
        prov.appendChild(provOpt);
    }
})();

/*根据所选的省份来显示城市列表*/
function showCity(obj) {
    var val = obj.options[obj.selectedIndex].value;
    if (val != current.prov) {
        current.prov = val;
        addrShow.value = '';
        btn.disabled = true;
        city.length = 1;
        country.length = 1;
    }

    if (val != '') {
        //查找省的索引
        var len = province.length;
        let provIndex = 0;
        for (var i = 0; i < len; i++) {
            if (val == province[i]['name']) {
                provIndex = i;
            }
        }

        var cityLen = province[provIndex]["city"].length;
        for (var j = 0; j < cityLen; j++) {
            var cityOpt = document.createElement('option');
            cityOpt.value = cityOpt.innerText = province[provIndex]["city"][j].name;
            city.appendChild(cityOpt);
        }
    }
}

/*根据所选的城市来显示县区列表*/
function showCountry(obj) {
    var val = obj.options[obj.selectedIndex].value;
    if (val != current.city) {
        current.city = val;
        addrShow.value = '';
        btn.disabled = true;
        country.length = 1; //清空之前的内容只留第一个默认选项
    }

    //查找省的索引
    var provLen = province.length;
    let provIndex = 0;
    for (var i = 0; i < provLen; i++) {
        if (current.prov == province[i]['name']) {
            provIndex = i;
            break;
        }
    }

    //查找城市的索引
    var cityLen = province[provIndex]["city"].length;
    let cityIndex = 0;
    for (var i = 0; i < cityLen; i++) {
        if (current.city == province[provIndex]["city"][i].name) {
            cityIndex = i;
            break;
        }
    }

    if (val != '') {
        var countryLen = province[provIndex]["city"][cityIndex].districtAndCounty.length;
        if (countryLen == 0) {
            addrShow.value = current.prov + '-' + current.city;
            return;
        }
        for (var n = 0; n < countryLen; n++) {
            var countryOpt = document.createElement('option');
            countryOpt.innerText = province[provIndex]["city"][cityIndex].districtAndCounty[n];
            countryOpt.value = province[provIndex]["city"][cityIndex].districtAndCounty[n];
            country.appendChild(countryOpt);
        }
    }
}

/*选择县区之后的处理函数*/
function selecCountry(obj) {
    current.country = obj.options[obj.selectedIndex].value;
    if ((current.city != '') && (current.country != '')) {
        btn.disabled = false;
    }
}

/*点击确定按钮显示用户所选的地址*/
function showAddr() {
    var fullAddress = current.prov + '-' + current.city + '-' + current.country;
    // 将地址赋值给 addr-show 输入框
    document.getElementById('addr-show').value = fullAddress;
    // 将地址值传递给隐藏的 address 字段
    document.getElementById('address').value = fullAddress;
}