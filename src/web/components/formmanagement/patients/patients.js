"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);


patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/assign', {
        templateUrl: '/components/formmanagement/patients/selectionmethod/patients-assign.html'
    });
}]);