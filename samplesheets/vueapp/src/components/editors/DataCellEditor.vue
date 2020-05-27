<template>
  <div v-if="value && renderInfo"
       :class="containerClasses">
    <!-- Value select -->
    <span v-if="editorType === 'select'">
      <select :ref="'input'"
              v-model="editValue"
              :class="'ag-cell-edit-input ' + getSelectClass()"
              @keydown="onKeyDown($event)">
        <option value="" :selected="selectEmptyValue(editValue)">-</option>
        <option v-for="(val, index) in editConfig.options"
                :key="index"
                :value="val"
                :selected="editValue === val">
          {{ val }}
        </option>
      </select>
    </span>
    <!-- Value basic input -->
    <span v-else>
      <input :ref="'input'"
             v-model="editValue"
             :class="'ag-cell-edit-input ' + getInputClasses()"
             :style="inputStyle"
             @keydown="onKeyDown($event)"
             :placeholder="getInputPlaceholder('Value')" />
    </span>
    <!-- Unit select (in popup) -->
    <select :ref="'unitText'"
            v-if="editConfig.hasOwnProperty('unit') &&
                  editConfig.unit.length > 0"
            v-model="editUnit"
            id="sodar-ss-vue-edit-select-unit"
            class="ag-cell-edit-input sodar-ss-vue-popup-input"
            :style="unitStyle">
      <option :value="null">-</option>
      <option v-for="(unit, index) in editConfig.unit"
              :key="index"
              :value="unit">
        {{ unit }}
      </option>
    </select>
  </div>
</template>

<script>
import Vue from 'vue'

const navKeyCodes = [33, 34, 35, 36, 37, 38, 39, 40]

// TODO: Update for support and validation for NAME colType
export default Vue.extend({
  data () {
    return {
      app: null,
      headerInfo: null,
      renderInfo: null,
      editConfig: null,
      editorType: 'text',
      regex: null,
      valid: true,
      invalidMsg: null,
      objCls: null,
      headerType: null,
      value: null,
      editValue: '',
      ogEditValue: '',
      editUnitEnabled: false,
      editUnit: '',
      ogEditUnit: '',
      containerClasses: '',
      inputStyle: '',
      unitStyle: '',
      nameValues: []
    }
  },
  methods: {
    /* Implemented ag-grid editor methods ----------------------------------- */
    getValue () {
      return this.value
    },
    isPopup () {
      // Show popup editor if unit can be changed
      if (this.editUnitEnabled) {
        return true
      }
      return false
    },
    getPopupPosition () {
      return 'over'
    },
    isCancelBeforeStart () {
      return false
    },
    isCancelAfterEnd () {
      return true
    },
    /* Event handling ------------------------------------------------------- */
    onKeyDown (event) {
      const keyCode = this.getKeyCode(event)

      // Handle navigation keycodes
      // TODO: Better way to do this? event.stopPropagation() fails (see #690)
      if (navKeyCodes.indexOf(keyCode) !== -1) {
        let caretPos = event.currentTarget.selectionStart

        if (keyCode === 33 || keyCode === 36) { // PgUp/Home
          caretPos = 0
        } else if (keyCode === 34 || keyCode === 35) { // PgDown/End
          caretPos = event.currentTarget.value.length
        } else if (keyCode === 37) { // Left
          if (caretPos >= 1) {
            caretPos = caretPos - 1
          } else {
            caretPos = 0
          }
        } else if (keyCode === 39) { // Right
          caretPos = caretPos + 1
        }

        this.$nextTick(() => {
          event.currentTarget.setSelectionRange(caretPos, caretPos)
        })
      }
    },
    /* Helpers -------------------------------------------------------------- */
    selectEmptyValue (value) {
      return value === '' || !value
    },
    getKeyCode (event) {
      return (typeof event.which === 'undefined') ? event.keyCode : event.which
    },
    getSelectClass () {
      if (navigator.userAgent.search('Firefox') > -1) {
        return 'sodar-ss-vue-select-firefox'
      }
    },
    getInputClasses () {
      let classes = ''
      if (!this.valid) {
        classes = classes + ' text-danger'
      }
      return classes + ' text-' + this.renderInfo.align
    },
    getInputPlaceholder (text) {
      if (this.isPopup() && this.editUnitEnabled) {
        return text
      }
      return ''
    },
    getValidState () {
      if (this.headerInfo.header_type === 'name') { // Name is a special case
        if (this.editValue.length === 0 ||
            (this.editValue !== this.ogEditValue &&
            this.nameValues.includes(this.editValue))) {
          return false
        }
      } else if (this.editValue !== '') {
        // Test range
        if (['integer', 'double'].includes(this.editConfig.format) &&
            'range' in this.editConfig &&
            this.editConfig.range.length === 2) {
          const range = this.editConfig.range
          const valNum = parseFloat(this.editValue)
          if (valNum < parseFloat(range[0]) ||
              valNum > parseFloat(range[1])) {
            this.invalidMsg = 'Not in Range (' +
              parseInt(range[0]) + '-' + parseInt(range[1]) + ')'
            return false
          }
        }
      }
      // Test Regex
      return !(this.editValue !== '' &&
          this.regex &&
          !this.regex.test(this.editValue)
      )
    },
    getUpdateData () {
      return Object.assign(
        this.value, this.headerInfo, { og_value: this.ogEditValue })
    },
    addNameValues (rowNode) {
      if (this.params.colDef.field in rowNode.data) {
        const value = rowNode.data[this.params.colDef.field]
        if (value.uuid !== this.value.uuid &&
            !this.nameValues.includes(value.value)) {
          this.nameValues.push(value.value)
        }
      }
    }
  },
  created () {
    this.app = this.params.app
    this.app.selectEnabled = false // Disable editing
    this.value = this.params.value
    this.editValue = this.params.value.value
    this.ogEditValue = this.editValue
    this.headerInfo = this.params.headerInfo
    this.renderInfo = this.params.renderInfo
    this.editConfig = this.params.editConfig

    // Set up unit value
    // TODO: Support ontology references for units
    if ('unit' in this.editConfig &&
        this.editConfig.unit.length > 0) {
      if ('unit' in this.value &&
          this.value.unit) {
        this.editUnit = this.value.unit
        this.ogEditUnit = this.value.unit
      } else if ('unit_default' in this.editConfig &&
          this.editConfig.unit_default.length > 0) {
        this.editUnit = this.editConfig.unit_default
      }
      this.editUnitEnabled = true
    }

    // Get initial valid state on existing value
    this.valid = this.getValidState()

    // Set classes and styling for popup
    if (this.isPopup()) {
      this.containerClasses = 'sodar-ss-vue-edit-popup text-nowrap'

      let inputWidth = this.renderInfo.width
      if (this.editUnitEnabled) {
        const unitWidth = Math.max(0, ...this.editConfig.unit.map(el => el.length)) * 15 + 30
        inputWidth = Math.max(inputWidth - unitWidth, 120)
        this.unitStyle = 'width: ' + unitWidth.toString() + 'px !important;'
      }
      this.inputStyle = 'width: ' + inputWidth.toString() + 'px;'
    }

    // Set editor type
    if (this.editConfig.format === 'select' &&
        'options' in this.editConfig && // Options
        this.editConfig.options.length > 0) {
      this.editorType = 'select'
    } else { // Basic text/integer/etc input
      this.editorType = 'basic'
    }

    // Set regex
    if (this.editConfig.format !== 'select' &&
        'regex' in this.editConfig &&
        this.editConfig.regex.length > 0) {
      this.regex = new RegExp(this.editConfig.regex)
    } else if (this.headerInfo.header_type === 'name') { // Name is special
      this.regex = /^([A-Za-z0-9-_]*)$/
    } else { // Default regex for certain fields
      if (this.editConfig.format === 'integer') {
        this.regex = /^(([1-9][0-9]*)|([0]?))$/ // TODO: TBD: Allow negative?
      } else if (this.editConfig.format === 'double') {
        this.regex = /^-?[0-9]+\.[0-9]+?$/
      }
    }

    // If name, get other current values for comparison in validation
    // TODO: Optimize by only searching in the relevant assay/study table
    if (this.headerInfo.header_type === 'name') {
      const gridUuids = this.app.getStudyGridUuids()

      for (let i = 0; i < gridUuids.length; i++) {
        const gridOptions = this.app.getGridOptionsByUuid(gridUuids[i])
        const gridApi = gridOptions.api
        if (!gridOptions.columnApi.getColumn(this.params.colDef.field)) {
          continue // Skip this grid if the column is not present
        }
        gridApi.forEachNode(this.addNameValues)
      }
    }

    // Prevent keyboard navigation in parent when editing
    // See onKeyDown() for manual in-cell editing
    this.params.colDef.suppressKeyboardEvent = function (params) {
      if (params.event.shiftKey) { // Key combinations break event keyCode
        return false
      }
      return navKeyCodes.indexOf(params.event.keyCode) !== -1
    }
  },
  mounted () {
    Vue.nextTick(() => {
      if (this.$refs.input) {
        this.$refs.input.focus()
      }
    })
  },
  updated () {
    this.valid = this.getValidState()
    this.value.value = this.editValue
    if (this.editUnitEnabled) {
      this.value.unit = this.editUnit
    }
  },
  beforeDestroy () {
    if (!this.valid) {
      this.value.value = this.ogEditValue
      this.value.unit = this.ogEditUnit
      this.app.showNotification(this.invalidMsg || 'Invalid value', 'danger', 1000)
    } else if (this.ogEditValue !== this.editValue ||
        (this.editUnitEnabled &&
          this.editValue &&
          this.ogEditUnit !== this.editUnit)) {
      // Set unit
      if (this.value.unit === '' || !this.value.value) {
        this.value.unit = null
      } else {
        this.value.unit = this.editUnit
      }
      this.app.handleCellEdit(this.getUpdateData(), true)
    }
    this.params.colDef.suppressKeyboardEvent = false
    this.app.selectEnabled = true
  }
})
</script>

<style scoped>

.sodar-ss-vue-edit-popup {
  border: 1px solid #6c757d;
  background: #ffffff;
  padding: 10px;
}

input.ag-cell-edit-input {
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;

  border: 0;
  width: 100%;
  height: 38px !important;
  background-color: #ffffd8 !important;
  padding-left: 11px;
  padding-right: 14px;
  padding-top: 0;
  padding-bottom: 2px;
}

select.ag-cell-edit-input {
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;

  border: 0;
  width: 100%;
  height: 38px !important;
  background-color: #ffffd8 !important;
  background-repeat: no-repeat;
  background-size: 0.5em auto;
  background-position: right 0.25em center;
  padding-left: 12px;
  padding-right: 18px;
  padding-top: 0;
  padding-bottom: 2px !important;

  background-image: url("data:image/svg+xml;charset=utf-8, \
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 40'> \
      <polygon points='0,0 60,0 30,40' style='fill:black;'/> \
    </svg>");
}

select#sodar-ss-vue-edit-select-unit {
  margin-left: 4px;
}

.sodar-ss-vue-select-firefox {
  padding-left: 8px !important;
}

input.sodar-ss-vue-popup-input,
select.sodar-ss-vue-popup-input {
  border: 1px solid #ced4da;
  border-radius: .25rem;
}

</style>