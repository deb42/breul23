"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var intern = angular.module("breul.intern", [
    "ngRoute",
    "breul.api"
]);


intern.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/application', {
        templateUrl: '/components/breul/intern/intern.html'
    });
}]);

