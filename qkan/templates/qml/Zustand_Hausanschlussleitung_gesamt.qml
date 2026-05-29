<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|Actions|MapTips|AttributeTable|Rendering|CustomProperties|Temporal|Notes" simplifyMaxScale="1" simplifyDrawingHints="1" simplifyLocal="1" labelsEnabled="0" symbologyReferenceScale="-1" readOnly="0" hasScaleBasedVisibilityFlag="0" minScale="100000000" simplifyDrawingTol="1" version="3.28.13-Firenze" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal startExpression="to_date(&quot;untersuchtag&quot;)" fixedDuration="0" durationUnit="min" limitMode="0" endExpression="to_date(&quot;untersuchtag&quot;)" durationField="" accumulate="0" mode="4" enabled="0" endField="" startField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 referencescale="-1" symbollevels="0" attr="min(max_ZD, max_ZB, max_ZS)" type="categorizedSymbol" forceraster="0" enableorderby="0">
    <categories>
      <category render="true" value="0" type="string" symbol="0" label="Zustandsklasse 0, starker Mangel, Gefahr in Verzug"/>
      <category render="true" value="1" type="string" symbol="1" label="Zustandsklasse 1, starker Mangel"/>
      <category render="true" value="2" type="string" symbol="2" label="Zustandsklasse 2, mittlerer Mangel"/>
      <category render="true" value="3" type="string" symbol="3" label="Zustandsklasse 3, leichter Mangel"/>
      <category render="true" value="4" type="string" symbol="4" label="Zustandsklasse 4, geringfügiger Mangel"/>
      <category render="true" value="5" type="string" symbol="5" label="Zustandsklasse 5, kein Mangel"/>
      <category render="true" value="" type="string" symbol="6" label="nicht ermittelt"/>
    </categories>
    <symbols>
      <symbol name="0" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="255,21,21,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="255,127,0,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="255,255,0,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="143,207,79,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="0,175,79,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="0,127,255,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.5"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="6" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="203,203,203,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.26"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" type="line" is_animated="0" force_rhr="0" frame_rate="10" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="255,127,0,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.26"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <Option type="Map">
      <Option name="QFieldSync/action" type="QString" value="copy"/>
      <Option name="QFieldSync/attachment_naming" type="QString" value="{}"/>
      <Option name="QFieldSync/cloud_action" type="QString" value="offline"/>
      <Option name="QFieldSync/geometry_locked_expression" type="QString" value=""/>
      <Option name="QFieldSync/photo_naming" type="QString" value="{}"/>
      <Option name="QFieldSync/relationship_maximum_visible" type="QString" value="{}"/>
      <Option name="QFieldSync/tracking_distance_requirement_minimum_meters" type="int" value="30"/>
      <Option name="QFieldSync/tracking_erroneous_distance_safeguard_maximum_meters" type="int" value="1"/>
      <Option name="QFieldSync/tracking_measurement_type" type="int" value="0"/>
      <Option name="QFieldSync/tracking_time_requirement_interval_seconds" type="int" value="30"/>
      <Option name="QFieldSync/value_map_button_interface_threshold" type="int" value="0"/>
      <Option name="dualview/previewExpressions" type="List">
        <Option type="QString" value="leitnam + ' (' + untersuchtag + ')'"/>
      </Option>
      <Option name="embeddedWidgets/count" type="int" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="pk" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="leitnam" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bezugspunkt" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Rohranfang" type="QString" value="Rohranfang"/>
              </Option>
              <Option type="Map">
                <Option name="Gerinnemittelpunkt" type="QString" value="Gerinnemittelpunkt"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="schoben" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schunten" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hoehe" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="breite" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="laenge" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="baujahr" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="untersuchtag" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="untersucher" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="untersuchrichtung" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="wetter" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bewertungsart" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bewertungstag" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="strasse" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="datenart" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="auftragsbezeichnung" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="max_ZD" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="max_ZB" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="max_ZS" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="xschob" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="yschob" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="xschun" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="yschun" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="kommentar" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="createdat" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd.MM.yyyy HH:mm:ss"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd HH:mm:ss"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="pk"/>
    <alias name="" index="1" field="leitnam"/>
    <alias name="Bezugspunkt" index="2" field="bezugspunkt"/>
    <alias name="Anfangsschacht" index="3" field="schoben"/>
    <alias name="Endschacht" index="4" field="schunten"/>
    <alias name="Profilhöhe" index="5" field="hoehe"/>
    <alias name="Profilbreite" index="6" field="breite"/>
    <alias name="Haltungslänge" index="7" field="laenge"/>
    <alias name="Baujahr" index="8" field="baujahr"/>
    <alias name="Inspektionsnr" index="9" field="id"/>
    <alias name="Inspektionsdatum" index="10" field="untersuchtag"/>
    <alias name="durchgeführt vom" index="11" field="untersucher"/>
    <alias name="" index="12" field="untersuchrichtung"/>
    <alias name="Wetter" index="13" field="wetter"/>
    <alias name="Bewertungsart" index="14" field="bewertungsart"/>
    <alias name="Bewertungstag" index="15" field="bewertungstag"/>
    <alias name="" index="16" field="strasse"/>
    <alias name="" index="17" field="datenart"/>
    <alias name="" index="18" field="auftragsbezeichnung"/>
    <alias name="" index="19" field="max_ZD"/>
    <alias name="" index="20" field="max_ZB"/>
    <alias name="" index="21" field="max_ZS"/>
    <alias name="" index="22" field="xschob"/>
    <alias name="" index="23" field="yschob"/>
    <alias name="" index="24" field="xschun"/>
    <alias name="" index="25" field="yschun"/>
    <alias name="Kommentar" index="26" field="kommentar"/>
    <alias name="bearbeitet" index="27" field="createdat"/>
  </aliases>
  <defaults>
    <default expression="" field="pk" applyOnUpdate="0"/>
    <default expression="" field="leitnam" applyOnUpdate="0"/>
    <default expression="" field="bezugspunkt" applyOnUpdate="0"/>
    <default expression="" field="schoben" applyOnUpdate="0"/>
    <default expression="" field="schunten" applyOnUpdate="0"/>
    <default expression="" field="hoehe" applyOnUpdate="0"/>
    <default expression="" field="breite" applyOnUpdate="0"/>
    <default expression="" field="laenge" applyOnUpdate="0"/>
    <default expression="" field="baujahr" applyOnUpdate="0"/>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="untersuchtag" applyOnUpdate="0"/>
    <default expression="" field="untersucher" applyOnUpdate="0"/>
    <default expression="" field="untersuchrichtung" applyOnUpdate="0"/>
    <default expression="" field="wetter" applyOnUpdate="0"/>
    <default expression="" field="bewertungsart" applyOnUpdate="0"/>
    <default expression="" field="bewertungstag" applyOnUpdate="0"/>
    <default expression="" field="strasse" applyOnUpdate="0"/>
    <default expression="" field="datenart" applyOnUpdate="0"/>
    <default expression="" field="auftragsbezeichnung" applyOnUpdate="0"/>
    <default expression="" field="max_ZD" applyOnUpdate="0"/>
    <default expression="" field="max_ZB" applyOnUpdate="0"/>
    <default expression="" field="max_ZS" applyOnUpdate="0"/>
    <default expression="" field="xschob" applyOnUpdate="0"/>
    <default expression="" field="yschob" applyOnUpdate="0"/>
    <default expression="" field="xschun" applyOnUpdate="0"/>
    <default expression="" field="yschun" applyOnUpdate="0"/>
    <default expression="" field="kommentar" applyOnUpdate="0"/>
    <default expression="" field="createdat" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="3" unique_strength="1" notnull_strength="1" exp_strength="0" field="pk"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="leitnam"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="bezugspunkt"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="schoben"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="schunten"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="hoehe"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="breite"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="laenge"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="baujahr"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="id"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="untersuchtag"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="untersucher"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="untersuchrichtung"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="wetter"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="bewertungsart"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="bewertungstag"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="strasse"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="datenart"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="auftragsbezeichnung"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="max_ZD"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="max_ZB"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="max_ZS"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="xschob"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="yschob"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="xschun"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="yschun"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="kommentar"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0" field="createdat"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="pk"/>
    <constraint exp="" desc="" field="leitnam"/>
    <constraint exp="" desc="" field="bezugspunkt"/>
    <constraint exp="" desc="" field="schoben"/>
    <constraint exp="" desc="" field="schunten"/>
    <constraint exp="" desc="" field="hoehe"/>
    <constraint exp="" desc="" field="breite"/>
    <constraint exp="" desc="" field="laenge"/>
    <constraint exp="" desc="" field="baujahr"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="untersuchtag"/>
    <constraint exp="" desc="" field="untersucher"/>
    <constraint exp="" desc="" field="untersuchrichtung"/>
    <constraint exp="" desc="" field="wetter"/>
    <constraint exp="" desc="" field="bewertungsart"/>
    <constraint exp="" desc="" field="bewertungstag"/>
    <constraint exp="" desc="" field="strasse"/>
    <constraint exp="" desc="" field="datenart"/>
    <constraint exp="" desc="" field="auftragsbezeichnung"/>
    <constraint exp="" desc="" field="max_ZD"/>
    <constraint exp="" desc="" field="max_ZB"/>
    <constraint exp="" desc="" field="max_ZS"/>
    <constraint exp="" desc="" field="xschob"/>
    <constraint exp="" desc="" field="yschob"/>
    <constraint exp="" desc="" field="xschun"/>
    <constraint exp="" desc="" field="yschun"/>
    <constraint exp="" desc="" field="kommentar"/>
    <constraint exp="" desc="" field="createdat"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{7f802d16-fd1e-45ac-9683-a33a61fc674b}" key="Canvas"/>
    <actionsetting id="{7f802d16-fd1e-45ac-9683-a33a61fc674b}" capture="1" isEnabledOnlyWhenEditable="0" name="Aktuelle Zustandsdaten für alle Hausanschlussleitungen anzeigen" icon="" shortTitle="Aktuelle Zustandsdaten" notificationMessage="" action="from qkan.tools.zeige_untersuchungsdaten import ShowHausanschlussschaeden&#xd;&#xa;&#xd;&#xa;form = ShowHausanschlussschaeden(id = 1)&#xd;&#xa;del form&#xd;&#xa;" type="1">
      <actionScope id="Canvas"/>
      <actionScope id="Layer"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{33764888-a85a-479d-961f-e1e8dc370402}" capture="0" isEnabledOnlyWhenEditable="0" name="Aktuelle Zustandsdaten zu Hausanschlussleitung anzeigen" icon="" shortTitle="Aktuelle Zustandsdaten zu Hausanschlussleitung" notificationMessage="" action="from qkan.tools.zeige_untersuchungsdaten import ShowHaltungsschaeden&#xd;&#xa;form = ShowHausanschlussschaeden(untersuchleit = '[%leitnam%]', id = 1)&#xd;&#xa;del form&#xd;&#xa;" type="1">
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{f0ac47bb-207a-48d1-8d1d-b983bc11a172}" capture="1" isEnabledOnlyWhenEditable="0" name="Alle Zustandsdaten für alle Hausanschlussleitungen anzeigen" icon="" shortTitle="Alle Zustandsdaten" notificationMessage="" action="from qkan.tools.zeige_untersuchungsdaten import ShowHausanschlussschaeden&#xd;&#xa;&#xd;&#xa;form = ShowHausanschlussschaeden()&#xd;&#xa;del form&#xd;&#xa;" type="1">
      <actionScope id="Canvas"/>
      <actionScope id="Layer"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{df45edbe-ca08-43ef-85cf-7e9ae15140b0}" capture="1" isEnabledOnlyWhenEditable="0" name="Zustandsdaten zu Hausanschlussleitung und Untersuchungsdatum anzeigen" icon="" shortTitle="Zustandsdaten zu Hausanschlussleitung und Untersuchungsdatum" notificationMessage="" action="from qkan.tools.zeige_untersuchungsdaten import ShowHausanschlussschaeden&#xd;&#xa;&#xd;&#xa;form = ShowHausanschlussschaeden(untersuchleit = '[%leitnam%]', untersuchtag = '[%untersuchtag%]')&#xd;&#xa;del form&#xd;&#xa;&#xd;&#xa;" type="1">
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortOrder="1" actionWidgetStyle="dropDown" sortExpression="&quot;haltnam&quot;">
    <columns>
      <column name="pk" type="field" hidden="0" width="-1"/>
      <column name="leitnam" type="field" hidden="0" width="-1"/>
      <column name="bezugspunkt" type="field" hidden="0" width="-1"/>
      <column name="schoben" type="field" hidden="0" width="-1"/>
      <column name="schunten" type="field" hidden="0" width="-1"/>
      <column name="hoehe" type="field" hidden="0" width="-1"/>
      <column name="breite" type="field" hidden="0" width="-1"/>
      <column name="laenge" type="field" hidden="0" width="-1"/>
      <column name="baujahr" type="field" hidden="0" width="-1"/>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="untersuchtag" type="field" hidden="0" width="-1"/>
      <column name="untersucher" type="field" hidden="0" width="-1"/>
      <column name="untersuchrichtung" type="field" hidden="0" width="-1"/>
      <column name="wetter" type="field" hidden="0" width="-1"/>
      <column name="bewertungsart" type="field" hidden="0" width="-1"/>
      <column name="bewertungstag" type="field" hidden="0" width="-1"/>
      <column name="strasse" type="field" hidden="0" width="-1"/>
      <column name="datenart" type="field" hidden="0" width="-1"/>
      <column name="auftragsbezeichnung" type="field" hidden="0" width="-1"/>
      <column name="max_ZD" type="field" hidden="0" width="-1"/>
      <column name="max_ZB" type="field" hidden="0" width="-1"/>
      <column name="max_ZS" type="field" hidden="0" width="-1"/>
      <column name="xschob" type="field" hidden="0" width="-1"/>
      <column name="yschob" type="field" hidden="0" width="-1"/>
      <column name="xschun" type="field" hidden="0" width="-1"/>
      <column name="yschun" type="field" hidden="0" width="-1"/>
      <column name="kommentar" type="field" hidden="0" width="-1"/>
      <column name="createdat" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="auftragsbezeichnung" editable="1"/>
    <field name="baujahr" editable="1"/>
    <field name="bewertungsart" editable="1"/>
    <field name="bewertungstag" editable="1"/>
    <field name="bezugspunkt" editable="1"/>
    <field name="breite" editable="1"/>
    <field name="createdat" editable="1"/>
    <field name="datenart" editable="1"/>
    <field name="haltnam" editable="1"/>
    <field name="hoehe" editable="1"/>
    <field name="id" editable="1"/>
    <field name="kommentar" editable="1"/>
    <field name="laenge" editable="1"/>
    <field name="leitnam" editable="1"/>
    <field name="max_ZB" editable="1"/>
    <field name="max_ZD" editable="1"/>
    <field name="max_ZS" editable="1"/>
    <field name="pk" editable="1"/>
    <field name="schoben" editable="1"/>
    <field name="schunten" editable="1"/>
    <field name="strasse" editable="1"/>
    <field name="untersucher" editable="1"/>
    <field name="untersuchrichtung" editable="1"/>
    <field name="untersuchtag" editable="1"/>
    <field name="wetter" editable="1"/>
    <field name="xschob" editable="1"/>
    <field name="xschun" editable="1"/>
    <field name="yschob" editable="1"/>
    <field name="yschun" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="auftragsbezeichnung" labelOnTop="0"/>
    <field name="baujahr" labelOnTop="0"/>
    <field name="bewertungsart" labelOnTop="0"/>
    <field name="bewertungstag" labelOnTop="0"/>
    <field name="bezugspunkt" labelOnTop="0"/>
    <field name="breite" labelOnTop="0"/>
    <field name="createdat" labelOnTop="0"/>
    <field name="datenart" labelOnTop="0"/>
    <field name="haltnam" labelOnTop="0"/>
    <field name="hoehe" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="kommentar" labelOnTop="0"/>
    <field name="laenge" labelOnTop="0"/>
    <field name="leitnam" labelOnTop="0"/>
    <field name="max_ZB" labelOnTop="0"/>
    <field name="max_ZD" labelOnTop="0"/>
    <field name="max_ZS" labelOnTop="0"/>
    <field name="pk" labelOnTop="0"/>
    <field name="schoben" labelOnTop="0"/>
    <field name="schunten" labelOnTop="0"/>
    <field name="strasse" labelOnTop="0"/>
    <field name="untersucher" labelOnTop="0"/>
    <field name="untersuchrichtung" labelOnTop="0"/>
    <field name="untersuchtag" labelOnTop="0"/>
    <field name="wetter" labelOnTop="0"/>
    <field name="xschob" labelOnTop="0"/>
    <field name="xschun" labelOnTop="0"/>
    <field name="yschob" labelOnTop="0"/>
    <field name="yschun" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="auftragsbezeichnung" reuseLastValue="0"/>
    <field name="baujahr" reuseLastValue="0"/>
    <field name="bewertungsart" reuseLastValue="0"/>
    <field name="bewertungstag" reuseLastValue="0"/>
    <field name="bezugspunkt" reuseLastValue="1"/>
    <field name="breite" reuseLastValue="0"/>
    <field name="createdat" reuseLastValue="0"/>
    <field name="datenart" reuseLastValue="0"/>
    <field name="haltnam" reuseLastValue="0"/>
    <field name="hoehe" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="kommentar" reuseLastValue="0"/>
    <field name="laenge" reuseLastValue="0"/>
    <field name="leitnam" reuseLastValue="0"/>
    <field name="max_ZB" reuseLastValue="0"/>
    <field name="max_ZD" reuseLastValue="0"/>
    <field name="max_ZS" reuseLastValue="0"/>
    <field name="pk" reuseLastValue="0"/>
    <field name="schoben" reuseLastValue="0"/>
    <field name="schunten" reuseLastValue="0"/>
    <field name="strasse" reuseLastValue="0"/>
    <field name="untersucher" reuseLastValue="0"/>
    <field name="untersuchrichtung" reuseLastValue="0"/>
    <field name="untersuchtag" reuseLastValue="0"/>
    <field name="wetter" reuseLastValue="0"/>
    <field name="xschob" reuseLastValue="0"/>
    <field name="xschun" reuseLastValue="0"/>
    <field name="yschob" reuseLastValue="0"/>
    <field name="yschun" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>leitnam + ' (' + untersuchtag + ')'</previewExpression>
  <mapTip>[% leitnam + ' (' + untersuchtag + ')' %]</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
