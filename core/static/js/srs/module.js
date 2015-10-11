srsModule = angular.module('srs', []).config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

srsModule.directive('srsEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if (event.which === 13) {
                scope.$apply(function () {
                    scope.$eval(attrs.srsEnter);
                });
                event.preventDefault();
            }
        });
    };
});

srsModule.directive('srsFocus', function ($timeout) {
    return {
        scope: {trigger: '=srsFocus'},
        link: function (scope, element) {
            scope.$watch('trigger', function (value) {
                if (value === true) {
                    element[0].focus();
                    element[0].select();
                }
            });
        }
    };
});

srsModule.filter('percentage', ['$filter', function($filter) {
    return function(input, decimals) {
        return $filter('number')(input * 100, decimals) + '%';
    };
}]);