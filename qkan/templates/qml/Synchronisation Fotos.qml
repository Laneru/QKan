<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.14-Bratislava" styleCategories="Symbology|Forms|AttributeTable|Notes">
  <fieldConfiguration>
    <field name="pk">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pk_best">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pk_ext">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="aktion">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="status">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNullState"/>
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="1" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="untersuchtag">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="objekt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="datei">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="field" width="-1" hidden="0" name="status"/>
      <column type="field" width="-1" hidden="0" name="aktion"/>
      <column type="field" width="-1" hidden="0" name="name"/>
      <column type="field" width="-1" hidden="0" name="objekt"/>
      <column type="field" width="-1" hidden="0" name="untersuchtag"/>
      <column type="field" width="-1" hidden="0" name="datei"/>
      <column type="field" width="-1" hidden="0" name="pk"/>
      <column type="field" width="-1" hidden="0" name="pk_best"/>
      <column type="field" width="-1" hidden="0" name="pk_ext"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles>
      <style rule="status and aktion = 'hinzufügen'" background_color="#b2df8a" background_color_alpha="255" name="hinzufügen">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'hinzufügen'" text_color="#33a02c" text_color_alpha="255" name="hinzufügen nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style rule="status and aktion = 'ändern'" background_color="#fdbf6f" background_color_alpha="255" name="ändern">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'ändern'" text_color="#ff7f00" text_color_alpha="255" name="ändern nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.3,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style rule="status and aktion = 'löschen'" background_color="#fb9a99" background_color_alpha="255" name="löschen">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'löschen'" text_color="#e31a1c" text_color_alpha="255" name="löschen nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.3,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style text_color="#5500ff" name="redundant" rule="aktion = 'Bezeichnung im Bestand nicht eindeutig'" text_color_alpha="255" background_color_alpha="255" background_color="#e6d9ff">
        <font strikethrough="0" italic="1" bold="1" description="MS Shell Dlg 2,8.3,-1,5,75,1,0,0,0,0" underline="0" style=""/>
      </style>
      <style text_color="#9500ff" name="redundant extern" rule="aktion = 'Bezeichnung extern nicht eindeutig'" text_color_alpha="255" background_color_alpha="255" background_color="#efd9ff">
        <font strikethrough="0" italic="1" bold="1" description="MS Shell Dlg 2,8.3,-1,5,75,1,0,0,0,0" underline="0" style=""/>
      </style>
    </rowstyles>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS-Formulare können eine Python-Funktion haben,, die aufgerufen wird, wenn sich das Formular öffnet

Diese Funktion kann verwendet werden um dem Formular Extralogik hinzuzufügen.

Der Name der Funktion wird im Feld "Python Init-Function" angegeben
Ein Beispiel folgt:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="aktion" editable="0"/>
    <field name="datei" editable="0"/>
    <field name="name" editable="0"/>
    <field name="objekt" editable="0"/>
    <field name="pk" editable="0"/>
    <field name="pk_best" editable="0"/>
    <field name="pk_ext" editable="0"/>
    <field name="status" editable="1"/>
    <field name="untersuchtag" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="aktion" labelOnTop="0"/>
    <field name="datei" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="objekt" labelOnTop="0"/>
    <field name="pk" labelOnTop="0"/>
    <field name="pk_best" labelOnTop="0"/>
    <field name="pk_ext" labelOnTop="0"/>
    <field name="status" labelOnTop="0"/>
    <field name="untersuchtag" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="aktion"/>
    <field reuseLastValue="0" name="datei"/>
    <field reuseLastValue="0" name="name"/>
    <field reuseLastValue="0" name="objekt"/>
    <field reuseLastValue="0" name="pk"/>
    <field reuseLastValue="0" name="pk_best"/>
    <field reuseLastValue="0" name="pk_ext"/>
    <field reuseLastValue="0" name="status"/>
    <field reuseLastValue="0" name="untersuchtag"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <layerGeometryType>4</layerGeometryType>
</qgis>
