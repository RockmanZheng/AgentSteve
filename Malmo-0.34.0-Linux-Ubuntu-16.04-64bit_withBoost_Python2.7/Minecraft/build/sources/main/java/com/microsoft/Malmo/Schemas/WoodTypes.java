//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2018.05.18 at 01:32:50 AM CST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for WoodTypes.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="WoodTypes">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="oak"/>
 *     &lt;enumeration value="spruce"/>
 *     &lt;enumeration value="birch"/>
 *     &lt;enumeration value="jungle"/>
 *     &lt;enumeration value="acacia"/>
 *     &lt;enumeration value="dark_oak"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "WoodTypes")
@XmlEnum
public enum WoodTypes {

    @XmlEnumValue("oak")
    OAK("oak"),
    @XmlEnumValue("spruce")
    SPRUCE("spruce"),
    @XmlEnumValue("birch")
    BIRCH("birch"),
    @XmlEnumValue("jungle")
    JUNGLE("jungle"),
    @XmlEnumValue("acacia")
    ACACIA("acacia"),
    @XmlEnumValue("dark_oak")
    DARK_OAK("dark_oak");
    private final String value;

    WoodTypes(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static WoodTypes fromValue(String v) {
        for (WoodTypes c: WoodTypes.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
