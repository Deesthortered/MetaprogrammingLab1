/**
 * ORY Hydra
 * Welcome to the ORY Hydra HTTP API documentation. You will find documentation for all HTTP APIs here.
 *
 * OpenAPI spec version: latest
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 *
 * Swagger Codegen version: 2.2.3
 *
 * Do not edit the class manually.
 *
 */

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['ApiClient'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    module.exports = factory(require('../ApiClient'));
  } else {
    // Browser globals (root is window)
    if (!root.OryHydra) {
      root.OryHydra = {};
    }
    root.OryHydra.AcceptLoginRequest = factory(root.OryHydra.ApiClient);
  }
}(this, function(ApiClient) {
  'use strict';




  /**
   * The AcceptLoginRequest model module.
   * @module model/AcceptLoginRequest
   * @version latest
   */

  /**
   * Constructs a new <code>AcceptLoginRequest</code>.
   * @alias module:model/AcceptLoginRequest
   * @class
   * @param subject {String} Subject is the user ID of the end-user that authenticated.
   */
  var exports = function(subject) {
    var _this = this;






    _this['subject'] = subject;
  };

  /**
   * Constructs a <code>AcceptLoginRequest</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/AcceptLoginRequest} obj Optional instance to populate.
   * @return {module:model/AcceptLoginRequest} The populated <code>AcceptLoginRequest</code> instance.
   */
  exports.constructFromObject = function(data, obj) {
    if (data) {
      obj = obj || new exports();

      if (data.hasOwnProperty('acr')) {
        obj['acr'] = ApiClient.convertToType(data['acr'], 'String');
      }
      if (data.hasOwnProperty('context')) {
        obj['context'] = ApiClient.convertToType(data['context'], {'String': Object});
      }
      if (data.hasOwnProperty('force_subject_identifier')) {
        obj['force_subject_identifier'] = ApiClient.convertToType(data['force_subject_identifier'], 'String');
      }
      if (data.hasOwnProperty('remember')) {
        obj['remember'] = ApiClient.convertToType(data['remember'], 'Boolean');
      }
      if (data.hasOwnProperty('remember_for')) {
        obj['remember_for'] = ApiClient.convertToType(data['remember_for'], 'Number');
      }
      if (data.hasOwnProperty('subject')) {
        obj['subject'] = ApiClient.convertToType(data['subject'], 'String');
      }
    }
    return obj;
  }

  /**
   * ACR sets the Authentication AuthorizationContext Class Reference value for this authentication session. You can use it to express that, for example, a user authenticated using two factor authentication.
   * @member {String} acr
   */
  exports.prototype['acr'] = undefined;
  /**
   * Context is an optional object which can hold arbitrary data. The data will be made available when fetching the consent request under the \"context\" field. This is useful in scenarios where login and consent endpoints share data.
   * @member {Object.<String, Object>} context
   */
  exports.prototype['context'] = undefined;
  /**
   * ForceSubjectIdentifier forces the \"pairwise\" user ID of the end-user that authenticated. The \"pairwise\" user ID refers to the (Pairwise Identifier Algorithm)[http://openid.net/specs/openid-connect-core-1_0.html#PairwiseAlg] of the OpenID Connect specification. It allows you to set an obfuscated subject (\"user\") identifier that is unique to the client.  Please note that this changes the user ID on endpoint /userinfo and sub claim of the ID Token. It does not change the sub claim in the OAuth 2.0 Introspection.  Per default, ORY Hydra handles this value with its own algorithm. In case you want to set this yourself you can use this field. Please note that setting this field has no effect if `pairwise` is not configured in ORY Hydra or the OAuth 2.0 Client does not expect a pairwise identifier (set via `subject_type` key in the client's configuration).  Please also be aware that ORY Hydra is unable to properly compute this value during authentication. This implies that you have to compute this value on every authentication process (probably depending on the client ID or some other unique value).  If you fail to compute the proper value, then authentication processes which have id_token_hint set might fail.
   * @member {String} force_subject_identifier
   */
  exports.prototype['force_subject_identifier'] = undefined;
  /**
   * Remember, if set to true, tells ORY Hydra to remember this user by telling the user agent (browser) to store a cookie with authentication data. If the same user performs another OAuth 2.0 Authorization Request, he/she will not be asked to log in again.
   * @member {Boolean} remember
   */
  exports.prototype['remember'] = undefined;
  /**
   * RememberFor sets how long the authentication should be remembered for in seconds. If set to `0`, the authorization will be remembered for the duration of the browser session (using a session cookie).
   * @member {Number} remember_for
   */
  exports.prototype['remember_for'] = undefined;
  /**
   * Subject is the user ID of the end-user that authenticated.
   * @member {String} subject
   */
  exports.prototype['subject'] = undefined;



  return exports;
}));


