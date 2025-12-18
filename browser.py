import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QToolBar, QAction, QLineEdit, QWidget, QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Browser")
        self.setGeometry(100, 100, 1200, 800)

        # ---------- Tabs ----------
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_from_tab)
        self.setCentralWidget(self.tabs)

        # ---------- Toolbar ----------
        nav = QToolBar()
        self.addToolBar(nav)

        back_btn = QAction("◀", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        nav.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        nav.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav.addWidget(self.url_bar)

        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.add_tab)
        nav.addAction(new_tab_btn)

        # Shortcuts
        new_tab_btn.setShortcut("Ctrl+T")

        close_tab_action = QAction(self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(
            lambda: self.close_tab(self.tabs.currentIndex())
        )
        self.addAction(close_tab_action)

        # First tab
        self.add_tab(home=True)

    # ---------- Tab Logic ----------
    def add_tab(self, home=False):
        browser = QWebEngineView()
        browser.urlChanged.connect(self.update_url)
        browser.titleChanged.connect(
            lambda title, b=browser: self.tabs.setTabText(
                self.tabs.indexOf(b), title[:18] or "New Tab"
            )
        )

        if home:
            path = os.path.abspath("homepage.html")
            browser.setUrl(QUrl.fromLocalFile(path))
        else:
            browser.setUrl(QUrl("https://duckduckgo.com"))

        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    # ---------- Navigation ----------
    def navigate_home(self):
        path = os.path.abspath("homepage.html")
        self.current_browser().setUrl(QUrl.fromLocalFile(path))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, qurl):
        if self.current_browser() == self.sender():
            self.url_bar.setText(qurl.toString())

    def update_url_from_tab(self, index):
        browser = self.tabs.widget(index)
        if browser:
            self.url_bar.setText(browser.url().toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())