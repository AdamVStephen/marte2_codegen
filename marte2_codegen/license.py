# TODO: Ensure license start/end markers are made so that we can iterate over a project
#       and do a global search/replace of license content.  Or point at one file rather
#       than repeating the license everywhere.

LICENSE_UKAEA ="""###################################################################
# LICENSE
#
# Copyright 2022 United Kingdom Atomic Energy Authority
#
# Licensing terms of this software have yet to be approved.
###################################################################"""

LICENSE_CCFE = """###################################################################
# LICENSE
#
# Copyright 2022 Culham Center for Fusion Energy
#
# Licensing terms of this software have yet to be approved.
###################################################################"""

LICENSE_UKAEA_EUPL_11_2022 ="""###################################################################
# LICENSE
#
# Copyright 2022 United Kingdom Atomic Energy Authority
#
# * Licensed under the EUPL, Version 1.1 or - as soon they will be approved
 * by the European Commission - subsequent versions of the EUPL (the "Licence")
 * You may not use this work except in compliance with the Licence.
 * You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
 *
 * @warning Unless required by applicable law or agreed to in writing, 
 * software distributed under the Licence is distributed on an "AS IS"
 * basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the Licence permissions and limitations under the Licence.
 *Licensing terms of this software have yet to be approved.
###################################################################"""


CPP_LICENSE_COPYRIGHT_UKAEA_EUPL_2022="""/*
 * @copyright 2022 United Kingdom Atomic Energy Authority
 *
 * Licensed under the EUPL, Version 1.1 or - as soon they will be approved
 * by the European Commission - subsequent versions of the EUPL (the "Licence")
 * You may not use this work except in compliance with the Licence.
 * You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
 *
 * @warning Unless required by applicable law or agreed to in writing, 
 * software distributed under the Licence is distributed on an "AS IS"
 * basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the Licence permissions and limitations under the Licence.
 */
"""

CPP_COPYRIGHT_UKAEA="""/*
 * @copyright United Kingdom Atomic Energy Authority
 *
 * Licensed under the EUPL, Version 1.1 or - as soon they will be approved
 * by the European Commission - subsequent versions of the EUPL (the "Licence")
 * You may not use this work except in compliance with the Licence.
 * You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
 *
 * @warning Unless required by applicable law or agreed to in writing, 
 * software distributed under the Licence is distributed on an "AS IS"
 * basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the Licence permissions and limitations under the Licence.
 */
"""

CPP_GAM_DETAILS_IMPLEMENTATION = """/*
 * @details This source file contains the definition of all the methods for
 * this function class (public, protected, and private). Be aware that some
 * methods, such as those inline could be defined on the header file, instead.
 */"""

CPP_DATASOURCE_DETAILS_IMPLEMENTATION = """/*
 * @details This source file contains the definition of all the methods for
 * this data source class (public, protected, and private). Be aware that some
 * methods, such as those inline could be defined on the header file, instead.
 */"""


# TODO : inject the class name into the details (double interpolation)

CPP_DETAILS_INTERFACE = """/*
 * @details This header file contains the declaration of the class 
 * with all of its public, protected and private members. It may also include
 * definitions for inline methods which need to be visible to the compiler.
 */"""
