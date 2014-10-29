"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var main = angular.module("breul.main", [
    "ngRoute",
    "breul.main"
]);

main.controller("mainCtrl", ["$scope", "Session", function ($scope, Session) {
    $scope.session = Session.get();
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: '/components/breul/main/main.html'
    });
}]);