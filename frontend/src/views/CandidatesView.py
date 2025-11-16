from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox,
    QGroupBox, QComboBox
)
from PySide6.QtCore import Qt
from requests import HTTPError
import os

from services.api import (
    list_roles,
    get_candidates,
    create_candidate,
    get_candidate,
    update_candidate,
    delete_candidate,
)


class CandidatesView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.candidato_actual_id = None
        self.user_role = os.getenv("USER_ROLE", "recruiter")

        self._init_ui()
        self._connect_signals()
        self.recargar_roles()
        self.recargar_candidatos()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def _init_ui(self):
        layout_principal = QVBoxLayout(self)

        # ===== BOTÓN MOSTRAR/OCULTAR FORMULARIO =====
        self.btn_toggle_form = QPushButton("Ocultar formulario")
        layout_principal.addWidget(self.btn_toggle_form)

        # ===== FORMULARIO =====
        self.grupo_form = QGroupBox("Candidato")
        layout_form = QFormLayout()

        self.in_dni = QLineEdit()
        self.in_name = QLineEdit()

        self.in_role = QComboBox()

        self.in_experience = QTextEdit()
        self.in_location = QLineEdit()
        self.in_email = QLineEdit()
        self.in_phone = QLineEdit()

        self.in_status = QComboBox()
        self.in_status.addItems(["", "OPEN", "BLOCKED", "QUIET"])

        self.in_strength = QTextEdit()
        self.in_salary_range = QLineEdit()
        self.in_notes = QTextEdit()

        layout_form.addRow("DNI *", self.in_dni)
        layout_form.addRow("Nombre *", self.in_name)
        layout_form.addRow("Rol *", self.in_role)
        layout_form.addRow("Experiencia", self.in_experience)
        layout_form.addRow("Ubicación", self.in_location)
        layout_form.addRow("Email", self.in_email)
        layout_form.addRow("Teléfono", self.in_phone)
        layout_form.addRow("Status", self.in_status)
        layout_form.addRow("Strength", self.in_strength)
        layout_form.addRow("Rango salarial", self.in_salary_range)
        layout_form.addRow("Notas", self.in_notes)

        # Botones
        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_crear = QPushButton("Crear")
        self.btn_guardar = QPushButton("Guardar cambios")
        self.btn_eliminar = QPushButton("Eliminar")

        fila_botones = QHBoxLayout()
        fila_botones.addWidget(self.btn_nuevo)
        fila_botones.addWidget(self.btn_crear)
        fila_botones.addWidget(self.btn_guardar)
        fila_botones.addWidget(self.btn_eliminar)

        layout_form.addRow(fila_botones)

        if self.user_role != "admin":
            self.btn_eliminar.setEnabled(False)

        self.grupo_form.setLayout(layout_form)
        layout_principal.addWidget(self.grupo_form)

        # ===== LISTADO =====
        grupo_lista = QGroupBox("Candidatos")
        layout_lista = QVBoxLayout()

        barra = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        barra.addWidget(self.btn_recargar)
        barra.addStretch()
        layout_lista.addLayout(barra)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Rol", "Status",
            "Ubicación", "Email", "Teléfono",
            "Creado", "ID",
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        layout_lista.addWidget(self.tabla)
        grupo_lista.setLayout(layout_lista)
        layout_principal.addWidget(grupo_lista)

    def _connect_signals(self):
        self.btn_toggle_form.clicked.connect(self.toggle_formulario)
        self.btn_nuevo.clicked.connect(self.nuevo_candidato)
        self.btn_crear.clicked.connect(self.crear_candidato)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_eliminar.clicked.connect(self.eliminar_candidato)
        self.btn_recargar.clicked.connect(self.recargar_candidatos)
        self.tabla.cellClicked.connect(self.on_tabla_clicked)

    # -------------------------------------------------
    # FORMULARIO: mostrar / ocultar
    # -------------------------------------------------
    def toggle_formulario(self):
        visible = self.grupo_form.isVisible()
        self.grupo_form.setVisible(not visible)
        if visible:
            self.btn_toggle_form.setText("Mostrar formulario")
        else:
            self.btn_toggle_form.setText("Ocultar formulario")

    # -------------------------------------------------
    # ROLES
    # -------------------------------------------------
    def recargar_roles(self):
        try:
            roles = list_roles()
        except Exception:
            roles = []

        self.in_role.clear()
        for r in roles:
            self.in_role.addItem(r["name"], r["roleId"])

    # -------------------------------------------------
    # VALIDACIONES Y PAYLOAD
    # -------------------------------------------------
    def _validar(self) -> bool:
        if not self.in_dni.text().strip():
            QMessageBox.warning(self, "Validación", "El campo 'DNI' es obligatorio.")
            return False
        if not self.in_name.text().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Nombre' es obligatorio.")
            return False
        if not self.in_role.currentText().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Rol' es obligatorio.")
            return False
        return True

    def _payload_desde_formulario(self) -> dict:
        return {
            "dni": self.in_dni.text().strip(),
            "name": self.in_name.text().strip(),
            "role": self.in_role.currentText().strip(),
            "experience": self.in_experience.toPlainText().strip() or None,
            "location": self.in_location.text().strip() or None,
            "email": self.in_email.text().strip() or None,
            "phone": self.in_phone.text().strip() or None,
            "status": self.in_status.currentText() or None,
            "strength": self.in_strength.toPlainText().strip() or None,
            "salaryRange": self.in_salary_range.text().strip() or None,
            "notes": self.in_notes.toPlainText().strip() or None,
        }

    def _limpiar_formulario(self):
        self.candidato_actual_id = None
        self.in_dni.clear()
        self.in_name.clear()
        self.in_role.setCurrentIndex(0)
        self.in_experience.clear()
        self.in_location.clear()
        self.in_email.clear()
        self.in_phone.clear()
        self.in_status.setCurrentIndex(0)
        self.in_strength.clear()
        self.in_salary_range.clear()
        self.in_notes.clear()

    def _rellenar_formulario_desde_candidato(self, cand: dict):
        self.candidato_actual_id = cand.get("candidateId")

        self.in_dni.setText(cand.get("dni", "") or "")
        self.in_name.setText(cand.get("name", "") or "")

        role = cand.get("role", "")
        idx = self.in_role.findText(role)
        if idx >= 0:
            self.in_role.setCurrentIndex(idx)

        self.in_experience.setPlainText(cand.get("experience", "") or "")
        self.in_location.setText(cand.get("location", "") or "")
        self.in_email.setText(cand.get("email", "") or "")
        self.in_phone.setText(cand.get("phone", "") or "")

        status = cand.get("status") or ""
        idx = self.in_status.findText(status)
        self.in_status.setCurrentIndex(idx if idx >= 0 else 0)

        self.in_strength.setPlainText(cand.get("strength", "") or "")
        self.in_salary_range.setText(cand.get("salaryRange", "") or "")
        self.in_notes.setPlainText(cand.get("notes", "") or "")

    # -------------------------------------------------
    # ACCIONES
    # -------------------------------------------------
    def nuevo_candidato(self):
        self._limpiar_formulario()

    def crear_candidato(self):
        if not self._validar():
            return

        payload = self._payload_desde_formulario()

        try:
            create_candidate(payload)
            QMessageBox.information(self, "OK", "Candidato creado correctamente.")
            self._limpiar_formulario()
            self.recargar_candidatos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se ha podido crear el candidato:\n{e}")

    def recargar_candidatos(self):

        self.recargar_roles()
        
        try:
            candidatos = get_candidates()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se han podido cargar los candidatos:\n{e}")
            return

        self.tabla.setRowCount(0)

        for cand in candidatos:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)

            name = cand.get("name", "")
            role = cand.get("role", "")
            status = cand.get("status", "")
            location = cand.get("location", "")
            email = cand.get("email", "")
            phone = cand.get("phone", "")
            created_at = cand.get("createdAt", "")
            cand_id = cand.get("candidateId", "")

            item_name = QTableWidgetItem(str(name))
            item_name.setData(Qt.UserRole, cand_id)

            self.tabla.setItem(fila, 0, item_name)
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(role)))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(status)))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(location)))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(email)))
            self.tabla.setItem(fila, 5, QTableWidgetItem(str(phone)))
            self.tabla.setItem(fila, 6, QTableWidgetItem(str(created_at)))
            self.tabla.setItem(fila, 7, QTableWidgetItem(str(cand_id)))

    def on_tabla_clicked(self, fila: int, columna: int):
        item = self.tabla.item(fila, 0)
        if not item:
            return

        candidate_id = item.data(Qt.UserRole)
        if not candidate_id:
            return

        try:
            cand = get_candidate(candidate_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se ha podido cargar el candidato:\n{e}")
            return

        self._rellenar_formulario_desde_candidato(cand)

    def guardar_cambios(self):
        if not self.candidato_actual_id:
            QMessageBox.information(self, "Editar", "Primero selecciona un candidato.")
            return

        if not self._validar():
            return

        payload = self._payload_desde_formulario()

        try:
            update_candidate(self.candidato_actual_id, payload)
            QMessageBox.information(self, "OK", "Candidato actualizado correctamente.")
            self.recargar_candidatos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se ha podido actualizar el candidato:\n{e}")

    def eliminar_candidato(self):
        if not self.candidato_actual_id:
            QMessageBox.information(self, "Eliminar", "Primero selecciona un candidato.")
            return

        if QMessageBox.question(self, "Confirmar eliminación",
                                "¿Seguro que quieres eliminar este candidato?",
                                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return

        try:
            delete_candidate(self.candidato_actual_id)
            QMessageBox.information(self, "OK", "Candidato eliminado correctamente.")
            self._limpiar_formulario()
            self.recargar_candidatos()
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                QMessageBox.warning(self, "Permisos", "Solo admin puede eliminar candidatos.")
            else:
                QMessageBox.critical(self, "Error", f"No se ha podido eliminar el candidato:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se ha podido eliminar el candidato:\n{e}")
