"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var application = angular.module("breul.application", [
    "ngRoute",
    "breul.api"
]);

application.controller("applicationCtrl", ["$scope", "Session", function ($scope, Session) {
    $scope.session = Session.get();
}]);


application.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/application', {
        templateUrl: '/components/breul/application/application.html'
    });
}]);

