"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionnaire", [
    "ngRoute",
    "formmanagement.api"
]);


questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionnaire/followup', {
        templateUrl: '/components/formmanagement/questionnaire/questionnaire.html'
    });
}]);

