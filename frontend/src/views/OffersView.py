from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDateEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGroupBox, QLabel
)
from PySide6.QtCore import Qt, QDate
from requests import HTTPError

from services.api import (
    list_offers,
    create_offer,
    get_offer,
    list_roles,
    update_offer,
    delete_offer,
    create_process,
)


class OffersView(QWidget):
    """
    Gestión completa de ofertas:
    - Crear
    - Listar
    - Editar
    - Eliminar
    - Crear proceso automáticamente al crear oferta
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.oferta_actual_id = None
        self._init_ui()
        self._connect_signals()
        self.recargar_ofertas()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def _init_ui(self):
        layout_principal = QVBoxLayout(self)

        # ===== BOTÓN MOSTRAR/OCULTAR FORMULARIO =====
        self.btn_toggle_form = QPushButton("Ocultar formulario")
        layout_principal.addWidget(self.btn_toggle_form)

        # ===== FORMULARIO =====
        self.grupo_form = QGroupBox("Oferta")
        layout_form = QFormLayout()

        self.in_company = QLineEdit()
        self.in_contact = QLineEdit()

        self.in_end_date = QDateEdit()
        self.in_end_date.setCalendarPopup(True)
        self.in_end_date.setDate(QDate.currentDate())

        # --- ROLES OFICIALES ---
        self.in_role = QComboBox()
        self._cargar_roles_oficiales()

        self.in_salary = QLineEdit()

        self.in_modality = QComboBox()
        self.in_modality.addItems(["", "remoto", "híbrido", "presencial"])

        self.in_location = QLineEdit()
        self.in_description = QTextEdit()
        self.in_must = QTextEdit()
        self.in_nice = QTextEdit()
        self.in_notes = QTextEdit()

        help_must = QLabel("Must have: una línea por requisito")
        help_must.setStyleSheet("color: gray; font-size: 11px;")
        help_nice = QLabel("Nice to have: una línea por requisito")
        help_nice.setStyleSheet("color: gray; font-size: 11px;")

        layout_form.addRow("Empresa *", self.in_company)
        layout_form.addRow("Persona contacto *", self.in_contact)
        layout_form.addRow("Fin oferta *", self.in_end_date)
        layout_form.addRow("Rol *", self.in_role)
        layout_form.addRow("Salario", self.in_salary)
        layout_form.addRow("Modalidad", self.in_modality)
        layout_form.addRow("Ubicación", self.in_location)
        layout_form.addRow("Descripción", self.in_description)
        layout_form.addRow(help_must, self.in_must)
        layout_form.addRow(help_nice, self.in_nice)
        layout_form.addRow("Notas", self.in_notes)

        self.btn_crear = QPushButton("Crear nueva")
        self.btn_guardar = QPushButton("Guardar cambios")
        self.btn_eliminar = QPushButton("Eliminar oferta")

        fila_botones = QHBoxLayout()
        fila_botones.addWidget(self.btn_crear)
        fila_botones.addWidget(self.btn_guardar)
        fila_botones.addWidget(self.btn_eliminar)

        layout_form.addRow(fila_botones)

        self.grupo_form.setLayout(layout_form)
        layout_principal.addWidget(self.grupo_form)

        # ===== LISTADO =====
        grupo_lista = QGroupBox("Ofertas")
        layout_lista = QVBoxLayout()

        barra = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        barra.addWidget(self.btn_recargar)
        barra.addStretch()
        layout_lista.addLayout(barra)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels([
            "Empresa",
            "Rol",
            "Ubicación",
            "Modalidad",
            "Fin oferta",
            "Salario",
            "Creada",
            "Offer ID",
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
        self.btn_crear.clicked.connect(self.crear_oferta)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_eliminar.clicked.connect(self.eliminar_oferta)
        self.btn_recargar.clicked.connect(self.recargar_ofertas)
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
    # ROLES OFICIALES
    # -------------------------------------------------
    def _cargar_roles_oficiales(self):
        try:
            roles = list_roles()
        except Exception:
            roles = []

        self.in_role.clear()
        for r in roles:
            self.in_role.addItem(r["name"], r["roleId"])

    # -------------------------------------------------
    # FORMULARIO
    # -------------------------------------------------
    def _validar(self) -> bool:
        if not self.in_company.text().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Empresa' es obligatorio.")
            return False
        if not self.in_contact.text().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Persona contacto' es obligatorio.")
            return False
        if not self.in_role.currentText().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Rol' es obligatorio.")
            return False
        if not self.in_salary.text().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Salario' es obligatorio.")
            return False
        if not self.in_modality.currentText().strip():
            QMessageBox.warning(self, "Validación", "El campo 'Modalidad' es obligatorio.")
            return False
        return True

    def _payload_desde_formulario(self) -> dict:
        end_date = self.in_end_date.date().toString("yyyy-MM-dd")

        def texto_a_lista(texto: str) -> list[str]:
            return [l.strip() for l in texto.splitlines() if l.strip()]

        return {
            "companyName": self.in_company.text().strip(),
            "contactPerson": self.in_contact.text().strip(),
            "endDate": end_date,
            "role": self.in_role.currentText().strip(),
            "salary": self.in_salary.text().strip() or None,
            "modality": self.in_modality.currentText() or None,
            "location": self.in_location.text().strip() or None,
            "description": self.in_description.toPlainText().strip() or None,
            "mustHave": texto_a_lista(self.in_must.toPlainText()),
            "niceToHave": texto_a_lista(self.in_nice.toPlainText()),
            "notes": self.in_notes.toPlainText().strip() or None,
        }

    def _limpiar_formulario(self):
        self.oferta_actual_id = None
        self.in_company.clear()
        self.in_contact.clear()
        self.in_end_date.setDate(QDate.currentDate())
        self.in_role.setCurrentIndex(0)
        self.in_salary.clear()
        self.in_modality.setCurrentIndex(0)
        self.in_location.clear()
        self.in_description.clear()
        self.in_must.clear()
        self.in_nice.clear()
        self.in_notes.clear()

    def _rellenar_formulario_desde_oferta(self, offer: dict):
        self.oferta_actual_id = offer.get("offerId")

        self.in_company.setText(offer.get("companyName", "") or "")
        self.in_contact.setText(offer.get("contactPerson", "") or "")

        end_date = offer.get("endDate")
        if end_date:
            qd = QDate.fromString(end_date, "yyyy-MM-dd")
            if qd.isValid():
                self.in_end_date.setDate(qd)

        rol = offer.get("role", "")
        idx = self.in_role.findText(rol)
        if idx >= 0:
            self.in_role.setCurrentIndex(idx)

        salary = offer.get("salary")
        self.in_salary.setText(str(salary) if salary is not None else "")

        modality = offer.get("modality") or ""
        idx = self.in_modality.findText(modality)
        self.in_modality.setCurrentIndex(idx if idx >= 0 else 0)

        self.in_location.setText(offer.get("location", "") or "")
        self.in_description.setPlainText(offer.get("description", "") or "")
        self.in_must.setPlainText("\n".join(offer.get("mustHave") or []))
        self.in_nice.setPlainText("\n".join(offer.get("niceToHave") or []))
        self.in_notes.setPlainText(offer.get("notes", "") or "")

    # -------------------------------------------------
    # ACCIONES
    # -------------------------------------------------
    def crear_oferta(self):
        self._cargar_roles_oficiales()

        if not self._validar():
            return

        payload = self._payload_desde_formulario()

        try:
            offer = create_offer(payload)
            QMessageBox.information(self, "OK", "Oferta creada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error creando oferta", str(e))
            return

        # Crear proceso automáticamente
        try:
            create_process(offer["offerId"], recruiter=None, notes=None)
            QMessageBox.information(self, "OK", "Proceso creado automáticamente.")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Proceso",
                f"La oferta se creó pero el proceso falló:\n{e}"
            )

        self._limpiar_formulario()
        self.recargar_ofertas()

    def recargar_ofertas(self):
        self._cargar_roles_oficiales()

        try:
            ofertas = list_offers()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se han podido cargar las ofertas:\n{e}")
            return

        self.tabla.setRowCount(0)

        for offer in ofertas:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)

            company = offer.get("companyName", "")
            role = offer.get("role", "")
            location = offer.get("location", "")
            modality = offer.get("modality", "")
            end_date = offer.get("endDate", "")
            salary = offer.get("salary", "")
            created_at = offer.get("createdAt", "")
            offer_id = offer.get("offerId", "")

            item_company = QTableWidgetItem(str(company))
            item_company.setData(Qt.UserRole, offer_id)

            self.tabla.setItem(fila, 0, item_company)
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(role)))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(location)))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(modality)))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(end_date)))
            self.tabla.setItem(fila, 5, QTableWidgetItem(str(salary)))
            self.tabla.setItem(fila, 6, QTableWidgetItem(str(created_at)))
            self.tabla.setItem(fila, 7, QTableWidgetItem(str(offer_id)))

    def on_tabla_clicked(self, fila: int, columna: int):
        item = self.tabla.item(fila, 0)
        if not item:
            return

        offer_id = item.data(Qt.UserRole)
        if not offer_id:
            return

        try:
            offer = get_offer(offer_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se ha podido cargar la oferta:\n{e}")
            return

        self._rellenar_formulario_desde_oferta(offer)

    def guardar_cambios(self):
        if not self.oferta_actual_id:
            QMessageBox.information(self, "Editar", "Selecciona una oferta.")
            return

        if not self._validar():
            return

        payload = self._payload_desde_formulario()

        try:
            update_offer(self.oferta_actual_id, payload)
            QMessageBox.information(self, "OK", "Oferta actualizada.")
            self.recargar_ofertas()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_oferta(self):
        if not self.oferta_actual_id:
            QMessageBox.information(self, "Eliminar", "Selecciona una oferta.")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Seguro que quieres eliminar esta oferta?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        try:
            delete_offer(self.oferta_actual_id)
            QMessageBox.information(self, "OK", "Oferta eliminada.")
            self._limpiar_formulario()
            self.recargar_ofertas()
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                QMessageBox.warning(self, "Permisos", "No tienes permisos para eliminar (solo admin).")
            else:
                QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
