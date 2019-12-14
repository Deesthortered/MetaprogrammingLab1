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
    root.OryHydra.JsonWebKeySetGeneratorRequest = factory(root.OryHydra.ApiClient);
  }
}(this, function(ApiClient) {
  'use strict';




  /**
   * The JsonWebKeySetGeneratorRequest model module.
   * @module model/JsonWebKeySetGeneratorRequest
   * @version latest
   */

  /**
   * Constructs a new <code>JsonWebKeySetGeneratorRequest</code>.
   * @alias module:model/JsonWebKeySetGeneratorRequest
   * @class
   * @param alg {String} The algorithm to be used for creating the key. Supports \"RS256\", \"ES512\", \"HS512\", and \"HS256\"
   * @param kid {String} The kid of the key to be created
   * @param use {String} The \"use\" (public key use) parameter identifies the intended use of the public key. The \"use\" parameter is employed to indicate whether a public key is used for encrypting data or verifying the signature on data. Valid values are \"enc\" and \"sig\".
   */
  var exports = function(alg, kid, use) {
    var _this = this;

    _this['alg'] = alg;
    _this['kid'] = kid;
    _this['use'] = use;
  };

  /**
   * Constructs a <code>JsonWebKeySetGeneratorRequest</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/JsonWebKeySetGeneratorRequest} obj Optional instance to populate.
   * @return {module:model/JsonWebKeySetGeneratorRequest} The populated <code>JsonWebKeySetGeneratorRequest</code> instance.
   */
  exports.constructFromObject = function(data, obj) {
    if (data) {
      obj = obj || new exports();

      if (data.hasOwnProperty('alg')) {
        obj['alg'] = ApiClient.convertToType(data['alg'], 'String');
      }
      if (data.hasOwnProperty('kid')) {
        obj['kid'] = ApiClient.convertToType(data['kid'], 'String');
      }
      if (data.hasOwnProperty('use')) {
        obj['use'] = ApiClient.convertToType(data['use'], 'String');
      }
    }
    return obj;
  }

  /**
   * The algorithm to be used for creating the key. Supports \"RS256\", \"ES512\", \"HS512\", and \"HS256\"
   * @member {String} alg
   */
  exports.prototype['alg'] = undefined;
  /**
   * The kid of the key to be created
   * @member {String} kid
   */
  exports.prototype['kid'] = undefined;
  /**
   * The \"use\" (public key use) parameter identifies the intended use of the public key. The \"use\" parameter is employed to indicate whether a public key is used for encrypting data or verifying the signature on data. Valid values are \"enc\" and \"sig\".
   * @member {String} use
   */
  exports.prototype['use'] = undefined;



  return exports;
}));

