$._message = function (options) {
    options = options || {};
    var msg = options.msg || '';
    options.error_title = options.error_title || '错误';
    options.error_width = options.error_width || 500;
    options.error_height = options.error_height || 'auto';
    options.error_timeout = options.error_timeout || 0;

    $.messager.show({
        msg: msg,
        title: options.error_title,
        width: options.error_width,
        height: options.error_height,
        style:{right: '', bottom: ''},
        timeout: options.error_timeout
    });
};

$._ajax = function (options) {
    options = options || {};
    options.type = options.type || 'POST';
    options.async = options.async || true;
    options.dataType = options.dataType || 'json';
    options.error = options.error || function (jqXHR, textStatus, errorThrown) {
        var err = {__all__: []};
        if(jqXHR.status == 0){
            err.__all__.push('Unknown network error.');
        }
        if(jqXHR.status == 500){
            err.__all__.push('Unknown server error.');
        }
        if(err.__all__.length > 0){
            jqXHR.responseText = JSON.stringify(err);
        }
        options.msg = '<div class="error-msg">'
                    + '<p>状态文本: <span class="font-grey">'+textStatus+'</span></p>'
                    + '<p>状态代码: <span class="font-grey">'+jqXHR.status+'</span></p>'
                    + '<p>响应文本: <span class="font-grey">'+jqXHR.responseText+'</span></p>'
                    + '</div>';
        $._message(options);
    };

    $.ajax(options);
};

$._control = function(p, options){
    options = options || {};
    options.cache = options.cache || false;
    options.method = options.method || 'GET';
    options.dataType = options.dataType || 'json';
    options.queryParams = options.queryParams || {};
    options.onBeforeLoad = options.onBeforeLoad || function () {
        $(this).panel('clear');
    };
    $(p).panel(options);
};
