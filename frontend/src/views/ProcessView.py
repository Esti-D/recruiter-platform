from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QGroupBox,
    QComboBox, QListWidget, QListWidgetItem, QAbstractItemView
)
from PySide6.QtCore import Qt
import os

from services.api import (
    list_processes,
    get_process,
    update_process,
    delete_process,
    generate_candidates,
    list_roles
)


class ProcessView(QWidget):
    """
    Gestión de procesos:
    - Lista de procesos
    - Detalle de proceso (colapsable)
    - Roles similares
    - Lista de candidatos del proceso (editable en la tabla)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.proceso_actual_id: str | None = None
        self.proceso_actual_data: dict | None = None

        self.user_role = os.getenv("USER_ROLE", "recruiter")

        self._init_ui()
        self._connect_signals()

        # Por defecto:
        # - panel de proceso oculto
        # - candidatos visible
        # - lista de procesos visible
        self._set_panel_proceso_visible(False)
        self._set_panel_candidatos_visible(True)
        self._set_panel_lista_visible(True)

        self.recargar_procesos()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def _init_ui(self):
        layout_principal = QVBoxLayout(self)

        # ===== BOTONES DE CONTROL DE PANELES =====
        fila_toggles = QHBoxLayout()
        self.btn_toggle_proceso = QPushButton("Mostrar proceso")
        self.btn_toggle_candidatos = QPushButton("Ocultar candidatos")
        self.btn_toggle_lista = QPushButton("Ocultar lista procesos")

        fila_toggles.addWidget(self.btn_toggle_proceso)
        fila_toggles.addWidget(self.btn_toggle_candidatos)
        fila_toggles.addWidget(self.btn_toggle_lista)
        fila_toggles.addStretch()

        layout_principal.addLayout(fila_toggles)

        # ===== DETALLE DE PROCESO =====
        self.grupo_detalle = QGroupBox("Proceso")
        layout_detalle = QFormLayout()

        self.in_process_id = QLineEdit()
        self.in_process_id.setReadOnly(True)

        self.in_offer_id = QLineEdit()
        self.in_offer_id.setReadOnly(True)

        self.in_role_offer = QLineEdit()
        self.in_role_offer.setReadOnly(True)

        self.in_recruiter = QLineEdit()

        self.in_status = QComboBox()
        self.in_status.addItems(["OPEN", "PAUSED", "CLOSED"])

        self.in_notes = QTextEdit()

        layout_detalle.addRow("Process ID", self.in_process_id)
        layout_detalle.addRow("Offer ID", self.in_offer_id)
        layout_detalle.addRow("Rol oferta", self.in_role_offer)
        layout_detalle.addRow("Recruiter", self.in_recruiter)
        layout_detalle.addRow("Status", self.in_status)
        layout_detalle.addRow("Notas", self.in_notes)

        self.btn_guardar_proceso = QPushButton("Guardar proceso")
        self.btn_eliminar_proceso = QPushButton("Eliminar proceso")

        fila_botones_proc = QHBoxLayout()
        fila_botones_proc.addWidget(self.btn_guardar_proceso)
        fila_botones_proc.addWidget(self.btn_eliminar_proceso)

        if self.user_role != "admin":
            self.btn_eliminar_proceso.setEnabled(False)

        layout_detalle.addRow(fila_botones_proc)

        self.grupo_detalle.setLayout(layout_detalle)
        layout_principal.addWidget(self.grupo_detalle)

        # ===== ROLES SIMILARES =====
        self.grupo_roles = QGroupBox("Roles similares")
        layout_roles = QVBoxLayout()

        self.list_roles = QListWidget()
        self.list_roles.setSelectionMode(QAbstractItemView.MultiSelection)

        self.btn_cargar_roles = QPushButton("Recargar roles")
        self.btn_generar_candidatos = QPushButton("Generar lista candidatos")

        layout_roles.addWidget(self.btn_cargar_roles)
        layout_roles.addWidget(self.list_roles)
        layout_roles.addWidget(self.btn_generar_candidatos)

        self.grupo_roles.setLayout(layout_roles)
        layout_principal.addWidget(self.grupo_roles)

        # ===== CANDIDATOS DEL PROCESO =====
        self.grupo_cands = QGroupBox("Candidatos del proceso")
        layout_cands = QVBoxLayout()

        # Tabla de candidatos (editable)
        self.tabla_cands = QTableWidget(0, 7)
        self.tabla_cands.setHorizontalHeaderLabels([
            "Nombre",
            "Rol",
            "Experiencia",
            "Strength",
            "Rango salarial",
            "Estado",
            "Notas",
        ])
        self.tabla_cands.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Permitimos edición en la tabla
        self.tabla_cands.setEditTriggers(QTableWidget.AllEditTriggers)
        self.tabla_cands.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_cands.setSelectionMode(QAbstractItemView.SingleSelection)

        layout_cands.addWidget(self.tabla_cands)

        # Botón para guardar todos los cambios de candidatos
        self.btn_guardar_candidatos = QPushButton("Guardar cambios candidatos")
        layout_cands.addWidget(self.btn_guardar_candidatos)

        self.grupo_cands.setLayout(layout_cands)
        layout_principal.addWidget(self.grupo_cands)

        # ===== LISTADO PROCESOS =====
        self.grupo_lista = QGroupBox("Procesos")
        layout_lista = QVBoxLayout()

        barra = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        barra.addWidget(self.btn_recargar)
        barra.addStretch()
        layout_lista.addLayout(barra)

        self.tabla_procesos = QTableWidget(0, 6)
        self.tabla_procesos.setHorizontalHeaderLabels([
            "Process ID",
            "Offer ID",
            "Rol oferta",
            "Status",
            "Creado",
            "Cerrado",
        ])
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_procesos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_procesos.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_procesos.setEditTriggers(QTableWidget.NoEditTriggers)

        layout_lista.addWidget(self.tabla_procesos)
        self.grupo_lista.setLayout(layout_lista)

        layout_principal.addWidget(self.grupo_lista)

    # -------------------------------------------------
    # SIGNALS
    # -------------------------------------------------
    def _connect_signals(self):
        self.btn_recargar.clicked.connect(self.recargar_procesos)
        self.tabla_procesos.cellClicked.connect(self.on_proceso_clicked)

        self.btn_cargar_roles.clicked.connect(self.cargar_roles)
        self.btn_generar_candidatos.clicked.connect(self.generar_candidatos)

        self.btn_guardar_proceso.clicked.connect(self.guardar_proceso)
        self.btn_eliminar_proceso.clicked.connect(self.eliminar_proceso)

        self.btn_toggle_proceso.clicked.connect(self.toggle_panel_proceso)
        self.btn_toggle_candidatos.clicked.connect(self.toggle_panel_candidatos)
        self.btn_toggle_lista.clicked.connect(self.toggle_panel_lista)

        self.btn_guardar_candidatos.clicked.connect(self.guardar_cambios_candidatos)

    # -------------------------------------------------
    # VISIBILIDAD PANELES
    # -------------------------------------------------
    def _set_panel_proceso_visible(self, visible: bool):
        self.grupo_detalle.setVisible(visible)
        self.grupo_roles.setVisible(visible)
        self.btn_toggle_proceso.setText(
            "Ocultar proceso" if visible else "Mostrar proceso"
        )

    def _set_panel_candidatos_visible(self, visible: bool):
        self.grupo_cands.setVisible(visible)
        self.btn_toggle_candidatos.setText(
            "Ocultar candidatos" if visible else "Mostrar candidatos"
        )

    def _set_panel_lista_visible(self, visible: bool):
        self.grupo_lista.setVisible(visible)
        self.btn_toggle_lista.setText(
            "Ocultar lista procesos" if visible else "Mostrar lista procesos"
        )

    def toggle_panel_proceso(self):
        self._set_panel_proceso_visible(not self.grupo_detalle.isVisible())

    def toggle_panel_candidatos(self):
        self._set_panel_candidatos_visible(not self.grupo_cands.isVisible())

    def toggle_panel_lista(self):
        self._set_panel_lista_visible(not self.grupo_lista.isVisible())

    # -------------------------------------------------
    # FUNCIONES GENERALES
    # -------------------------------------------------
    def recargar_procesos(self):
        try:
            procesos = list_processes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pueden cargar los procesos.\n{e}")
            return

        self.tabla_procesos.setRowCount(0)

        for p in procesos:
            fila = self.tabla_procesos.rowCount()
            self.tabla_procesos.insertRow(fila)

            pid = p.get("processId")

            item_pid = QTableWidgetItem(pid)
            item_pid.setData(Qt.UserRole, pid)

            self.tabla_procesos.setItem(fila, 0, item_pid)
            self.tabla_procesos.setItem(fila, 1, QTableWidgetItem(p.get("offerId", "")))
            self.tabla_procesos.setItem(fila, 2, QTableWidgetItem(p.get("roleOffer", "")))
            self.tabla_procesos.setItem(fila, 3, QTableWidgetItem(p.get("status", "")))
            self.tabla_procesos.setItem(fila, 4, QTableWidgetItem(str(p.get("createdAt", ""))))
            self.tabla_procesos.setItem(fila, 5, QTableWidgetItem(str(p.get("closedAt", ""))))

        if procesos:
            self.on_proceso_clicked(0, 0)
        else:
            self._limpiar_detalle()
            self._rellenar_candidatos([])

    def on_proceso_clicked(self, fila, col):
        item = self.tabla_procesos.item(fila, 0)
        if not item:
            return

        pid = item.data(Qt.UserRole)
        if not pid:
            return

        try:
            p = get_process(pid)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se puede obtener el proceso.\n{e}")
            return

        self._rellenar_detalle(p)

    def _limpiar_detalle(self):
        self.proceso_actual_id = None
        self.proceso_actual_data = None
        self.in_process_id.clear()
        self.in_offer_id.clear()
        self.in_role_offer.clear()
        self.in_recruiter.clear()
        self.in_status.setCurrentIndex(0)
        self.in_notes.clear()
        self._rellenar_candidatos([])

    def _rellenar_detalle(self, p: dict):
        self.proceso_actual_id = p["processId"]
        self.proceso_actual_data = p

        self.in_process_id.setText(p["processId"])
        self.in_offer_id.setText(p["offerId"])
        self.in_role_offer.setText(p["roleOffer"])
        self.in_recruiter.setText(p.get("recruiter") or "")

        idx = self.in_status.findText(p.get("status", "OPEN"))
        if idx >= 0:
            self.in_status.setCurrentIndex(idx)

        self.in_notes.setPlainText(p.get("notes") or "")

        self.cargar_roles(preselected=p.get("similarRoles", []))
        self._rellenar_candidatos(p.get("candidates", []))

    # -------------------------------------------------
    # CANDIDATOS EN EL PROCESO
    # -------------------------------------------------
    def _rellenar_candidatos(self, lista):
        self.tabla_cands.setRowCount(0)

        for c in lista:
            fila = self.tabla_cands.rowCount()
            self.tabla_cands.insertRow(fila)

            # Nombre (no editable)
            item_name = QTableWidgetItem(c.get("name", ""))
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            # guardamos candidateId en UserRole
            item_name.setData(Qt.UserRole, c.get("candidateId"))
            self.tabla_cands.setItem(fila, 0, item_name)

            # Rol (no editable)
            item_role = QTableWidgetItem(c.get("role", ""))
            item_role.setFlags(item_role.flags() & ~Qt.ItemIsEditable)
            self.tabla_cands.setItem(fila, 1, item_role)

            # Estas columnas sí se podrán editar libremente
            self.tabla_cands.setItem(fila, 2, QTableWidgetItem(c.get("experience", "") or ""))
            self.tabla_cands.setItem(fila, 3, QTableWidgetItem(c.get("strength", "") or ""))
            self.tabla_cands.setItem(fila, 4, QTableWidgetItem(c.get("salaryRange", "") or ""))
            self.tabla_cands.setItem(fila, 5, QTableWidgetItem(c.get("state", "") or ""))
            self.tabla_cands.setItem(fila, 6, QTableWidgetItem(c.get("notes", "") or ""))

    def guardar_cambios_candidatos(self):
        """Lee la tabla de candidatos y guarda todos los cambios en el proceso."""
        if not self.proceso_actual_id:
            QMessageBox.information(self, "Proceso", "Selecciona un proceso.")
            return

        try:
            p = get_process(self.proceso_actual_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se puede obtener el proceso.\n{e}")
            return

        candidatos_originales = p.get("candidates", [])
        candidatos_por_id = {c.get("candidateId"): c for c in candidatos_originales}

        nuevos_candidatos = []

        for fila in range(self.tabla_cands.rowCount()):
            item_name = self.tabla_cands.item(fila, 0)
            if not item_name:
                continue

            cand_id = item_name.data(Qt.UserRole)
            if not cand_id:
                continue

            base = candidatos_por_id.get(cand_id, {}).copy()

            # mantenemos name y role del original
            base["candidateId"] = cand_id
            base["name"] = base.get("name", item_name.text())
            base["role"] = base.get("role", self.tabla_cands.item(fila, 1).text())

            base["experience"] = (self.tabla_cands.item(fila, 2).text() or "").strip() or None
            base["strength"] = (self.tabla_cands.item(fila, 3).text() or "").strip() or None
            base["salaryRange"] = (self.tabla_cands.item(fila, 4).text() or "").strip() or None
            base["state"] = (self.tabla_cands.item(fila, 5).text() or "").strip() or None
            base["notes"] = (self.tabla_cands.item(fila, 6).text() or "").strip() or None

            nuevos_candidatos.append(base)

        cambios = {"candidates": nuevos_candidatos}

        try:
            updated = update_process(self.proceso_actual_id, cambios)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pueden guardar los cambios de candidatos.\n{e}")
            return

        self._rellenar_detalle(updated)
        QMessageBox.information(self, "OK", "Candidatos actualizados en el proceso.")

    # -------------------------------------------------
    # ROLES SIMILARES
    # -------------------------------------------------
    def cargar_roles(self, preselected=None):
        preselected = preselected or []

        try:
            roles = list_roles()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pueden obtener los roles.\n{e}")
            return

        self.list_roles.clear()

        for r in roles:
            item = QListWidgetItem(r["name"])
            item.setData(Qt.UserRole, r["roleId"])

            if r["name"] in preselected:
                item.setSelected(True)

            self.list_roles.addItem(item)

    def generar_candidatos(self):
        if not self.proceso_actual_id:
            QMessageBox.information(self, "Proceso", "Selecciona un proceso.")
            return

        selected_roles = [i.text() for i in self.list_roles.selectedItems()]

        try:
            result = generate_candidates(self.proceso_actual_id, selected_roles)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se puede generar candidatos.\n{e}")
            return

        p = get_process(self.proceso_actual_id)
        self._rellenar_detalle(p)

        QMessageBox.information(
            self,
            "Candidatos generados",
            f"Se han añadido {result.get('count', 0)} candidatos al proceso."
        )

    # -------------------------------------------------
    # GUARDAR / ELIMINAR PROCESO
    # -------------------------------------------------
    def guardar_proceso(self):
        if not self.proceso_actual_id:
            QMessageBox.information(self, "Proceso", "Selecciona un proceso.")
            return

        changes = {
            "recruiter": self.in_recruiter.text().strip() or None,
            "status": self.in_status.currentText(),
            "notes": self.in_notes.toPlainText().strip() or None
        }

        try:
            updated = update_process(self.proceso_actual_id, changes)
            self._rellenar_detalle(updated)
            self.recargar_procesos()
            QMessageBox.information(self, "OK", "Proceso actualizado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se puede actualizar el proceso.\n{e}")

    def eliminar_proceso(self):
        if not self.proceso_actual_id:
            QMessageBox.information(self, "Proceso", "Selecciona un proceso.")
            return

        if self.user_role != "admin":
            QMessageBox.warning(self, "Permiso", "Solo admin puede eliminar procesos.")
            return

        try:
            delete_process(self.proceso_actual_id)
            self.recargar_procesos()
            QMessageBox.information(self, "OK", "Proceso eliminado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se puede eliminar.\n{e}")
