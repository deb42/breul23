"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var main = angular.module("formmanagement.main", [
    "ngRoute",
    "formmanagement.main"
]);

main.controller("mainCtrl", ["$scope", "Session", function ($scope, Session){
    $scope.session = Session.get();
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: '/components/formmanagement/main/main.html'
    });
}]);