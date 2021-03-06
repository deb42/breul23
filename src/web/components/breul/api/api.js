"use strict";

/**
 * breul API Module
 * Contains all client-side models and manages *all* communication with the backend.
 **/

var api = angular.module("breul.api", [
    "ngResource",
    "ui.bootstrap.modal",
    "ui.bootstrap.tpls"
]);


var TYPE_PATIENT = 1;
var TYPE_PHYSICIAN = 2;
var TYPE_ADMIN = 4;

api.constant("UserType", {
    "Patient": TYPE_PATIENT,
    "Physician": TYPE_PHYSICIAN,
    "Admin": TYPE_ADMIN
});
api.factory("getUserClass", [ "Patient" , "Physician", function (Patient, Physician) {
    return function getUserClass(type) {
        /* jshint bitwise: false*/
        if (type & TYPE_PHYSICIAN) {
            return Physician;
        }
        if (type & TYPE_PATIENT) {
            return Patient;
        }
    };
}]);

api.factory("Announcements", ["$resource", function ($resource) {
    return $resource("/api/announcements");
}]);

api.factory("Items", ["$resource", function ($resource) {
    return $resource("/api/items");
}]);

api.factory("SoldItemBar", ["$resource", function ($resource) {
    return $resource("/api/soldItemBar");
}]);

api.factory("Patient", ["$resource", function ($resource) {
    return $resource("/api/patients/:type", {type: "@type"});
}]);

api.factory("Announcements", ["$resource", function ($resource) {
    return $resource("/api/announcements");
}]);


api.factory("Physician", ["$resource", function ($resource) {
    return $resource("/api/physicians/:id", {id: "@id" });
}]);

api.factory("Questionnaire", ["$resource", function ($resource) {
    return $resource("/api/questionnaires/:id", {id: "@id" });
}]);

api.factory("Reply", ["$resource", function ($resource) {
            return $resource("/api/reply/:type/:id", {type: "@type", id: "@id"});
}]);

api.factory("DiagnosisParticipants", ["$resource", function ($resource) {
            return $resource("/api/diagnosis/participants/:patient", {patient: "@patient"});
}]);

api.factory("AssignedPatients", ["$resource", function ($resource) {
            return $resource("/api/diagnosis/patients");
}]);

api.service("Session", ["$http", "$q", "getUserClass", "Physician", "BarCharge",
    function ($http, $q, getUserClass, Physician, BarCharge) {
        var self = this;

        var cache_enabled = false;
        var sessionStorageKey = "session";

        var data = {};

        // set session details for new session
        var cacheSession = function (session) {
            if (!session) {
                delete sessionStorage[sessionStorageKey];
            }
            if (cache_enabled) {
                sessionStorage[sessionStorageKey] = JSON.stringify(session);
            }
        };

        // update existing session details
        var update = function (session) {
            cacheSession(session);
            console.log(session);
            //Replace this.data with the session info,
            //but make sure that the JS object reference to session.data doesn't change.
            for (var key in data) {
                delete data[key];
            }
            if (session && session.bar_charge) {
                data.bar_charge = session.bar_charge
            }
            if (session && session.user) {
                var UserClass = getUserClass(session.user.type);
                data.user = new UserClass(session.user);
            }
            if (session && session.physician) {
                data.physician = new Physician(session.physician);
            }
            if(session && session.bar_charge && session.user){
                BarCharge.setUserAuthenticated(session.bar_charge.barCharge.resident_id === session.user.id)
            }
        };
        var c = sessionStorage[sessionStorageKey];

        // Session.init indicates whether the session could be successfully established on page load.
        // Do not use this in your directives etc!
        // $scope.$watch() the object returned by Session.get() instead.
        var init;
        if (c) {
            var deferred = $q.defer();
            init = deferred.promise;
            update(JSON.parse(c));
            deferred.resolve(true);
        } else {
            update(undefined);
            init = $http.get("/api/session").success(function (session) {
                console.log(session)
                update(session);
            });
        }

        // login function
        self.login = function (auth) {
            return $http.post('/api/session', auth)
                .success(function (session) {
                    // set session data
                    update(session);
                });
        };

        // logout function
        self.logout = function () {
            return $http.delete('/api/session').success(function () {
                // delete session data
                update(undefined);
                // reload page to clean up JS session data
                window.location.reload();
            });
        };

        self.signup = function (patient) {
            return $http.post('/api/session/new', patient)
                .success(function (session) {
                    // set session data
                    update(session);
                });
        }

        // must be called before user.$save to persist updated session information in cache.
        self.updateCache = cacheSession;

        self.init = init;

        // Returns a read-only session object containing user information.
        self.get = function () {
            return data;
        };
    }]);

api.factory('showLoginDialog', ['$modal', '$http', '$location', 'Session', 'showSingUpDialog',
    function ($modal, $http, $location, Session, showSingUpDialog) {

        var LoginDialogCtrl = function ($scope, $modalInstance) {
            $scope.login = function (user) {
                $scope.noLogin = $scope.noUser = false;
                if (user && user.username && user.password) {
                    Session.login(user)
                        .success(function () {
                            $modalInstance.close();
                            $location.path('/announcements');
                            //window.location.reload();
                        })
                        .error(function () {
                            $scope.noLogin = true;
                        });
                }else{
                    $scope.noUser = true;
                }

            };
            $scope.new_patient = function () {
                showSingUpDialog();
                $modalInstance.close();
            };
        };



        return function showLoginDialog() {
            $modal.open({
                controller: LoginDialogCtrl,
                templateUrl: '/components/breul/login/login.html',
                keyboard: false,
                backdrop: "static"
            });
        };
    }
]);

