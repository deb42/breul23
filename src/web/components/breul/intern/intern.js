"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var intern = angular.module("breul.intern", [
    "ngRoute",
    "breul.api"
]);

main.controller("internCtrl", ["$scope", "Session", function ($scope, Session){
    $scope.session = Session.get();
}]);


intern.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/intern', {
        templateUrl: '/components/breul/intern/intern.html'
    });
}]);

