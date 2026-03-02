import os
import glob
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.utils import platform

# 导入转换函数（从 mesh_converter.py 中导入）
from mesh_converter import convert_mesh_to_obj

class MeshConverterApp(App):
    def build(self):
        # 主布局
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 标题
        title = Label(text='光遇 .mesh 转换器', size_hint=(1, 0.1), font_size='20sp')
        self.layout.add_widget(title)

        # 文件选择器区域
        self.filechooser = FileChooserListView(
            path=self.get_default_path(),
            filters=['*.mesh'],
            size_hint=(1, 0.6),
            multiselect=True
        )
        self.filechooser.bind(selection=self.on_selection)
        self.layout.add_widget(self.filechooser)

        # 按钮区域
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.convert_btn = Button(text='转换选中文件')
        self.convert_btn.bind(on_press=self.convert_files)
        btn_layout.add_widget(self.convert_btn)

        self.status_label = Label(text='就绪', size_hint=(0.7, 1))
        btn_layout.add_widget(self.status_label)

        self.layout.add_widget(btn_layout)

        # 结果列表区域（滚动显示转换结果）
        self.result_scroll = ScrollView(size_hint=(1, 0.2))
        self.result_grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.result_grid.bind(minimum_height=self.result_grid.setter('height'))
        self.result_scroll.add_widget(self.result_grid)
        self.layout.add_widget(self.result_scroll)

        # 请求权限（仅 Android）
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            except:
                pass

        return self.layout

    def get_default_path(self):
        if platform == 'android':
            # 尝试获取外部存储的 Download 目录
            try:
                from android.storage import primary_external_storage_path
                return primary_external_storage_path() + '/Download'
            except:
                return '/sdcard/Download'
        return '.'

    def on_selection(self, instance, value):
        self.selected_files = value
        self.status_label.text = f'已选择 {len(value)} 个文件'

    def convert_files(self, instance):
        if not hasattr(self, 'selected_files') or not self.selected_files:
            self.show_popup('提示', '请先选择要转换的文件')
            return

        # 禁用按钮防止重复点击
        self.convert_btn.disabled = True
        self.status_label.text = '转换中...'
        self.result_grid.clear_widgets()

        # 逐个转换（为了不阻塞 UI，使用 Clock 调度）
        self.conversion_index = 0
        self.success_count = 0
        self.fail_count = 0
        Clock.schedule_once(self.convert_next, 0.1)

    def convert_next(self, dt):
        if self.conversion_index >= len(self.selected_files):
            # 转换完成
            self.status_label.text = f'完成！成功 {self.success_count} / 失败 {self.fail_count}'
            self.convert_btn.disabled = False
            return

        file_path = self.selected_files[self.conversion_index]
        self.status_label.text = f'正在处理: {os.path.basename(file_path)}'

        try:
            # 调用转换函数，输出目录使用当前文件所在目录（或 Download 目录）
            output_dir = os.path.dirname(file_path)
            result = convert_mesh_to_obj(file_path, output_dir, mode='hybrid')
            if result['success']:
                status = f'✅ {os.path.basename(file_path)}: 顶点 {result["vertex_count"]}, 面 {result["face_count"]} (解析器: {result["parser"]})'
                self.success_count += 1
            else:
                status = f'❌ {os.path.basename(file_path)}: {result["error"]}'
                self.fail_count += 1
        except Exception as e:
            status = f'❌ {os.path.basename(file_path)}: 异常 {str(e)}'
            self.fail_count += 1

        # 添加到结果列表
        label = Label(
            text=status,
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle',
            text_size=(self.result_scroll.width - 20, None)
        )
        label.bind(size=label.setter('text_size'))  # 自动换行
        self.result_grid.add_widget(label)

        self.conversion_index += 1
        Clock.schedule_once(self.convert_next, 0.1)  # 继续下一个

    def show_popup(self, title, msg):
        popup = Popup(title=title, content=Label(text=msg), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == '__main__':
    MeshConverterApp().run()
