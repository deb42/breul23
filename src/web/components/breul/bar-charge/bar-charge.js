"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var barCharge = angular.module("breul.barCharge", [
    "ngRoute",
    "breul.barCharge"
]);

barCharge.controller("barChargeCtrl", ["$scope", "Session", "Items", function ($scope, Session, Items) {
    $scope.session = Session.get();
    $scope.items = Items.query();

    $scope.$watch("session.user", function () {

    });

}]);

barCharge.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/barCharge', {
        templateUrl: '/components/breul/bar-charge/bar-charge.html'
    });
}]);