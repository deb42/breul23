"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var announcements = angular.module("breul.announcements", [
    "ngRoute",
    "breul.announcements"
]);

announcements.controller("announcementsCtrl", ["$scope", "Session", "Announcements", function ($scope, Session, Announcements) {
    $scope.session = Session.get();

    $scope.$watch("session.user", function () {
        $scope.announcements = Announcements.query();
    });

}]);

announcements.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/announcements', {
        templateUrl: '/components/breul/announcements/announcements.html'
    });
}]);