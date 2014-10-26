"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("breul.patients", [
    "ngRoute",
    "breul.api"
]);


patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/assign', {
        templateUrl: '/components/breul/patients/selectionmethod/patients-assign.html'
    });
}]);