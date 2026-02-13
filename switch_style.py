import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print("=" * 40)
        print("错误页面风格管理器")
        print("=" * 40)
        print("1. 应用统一风格 (V1) - 极简磨砂玻璃")
        print("2. 应用多彩风格 (V2) - 颜色区分")
        print("3. 应用纹理风格 (V3) - 纹理与动画")
        print("4. 应用多布局风格 (V4) - 终端/门禁/分屏")
        print("5. 应用独特布局风格 (V5) - 每种错误独立设计")
        print("6. 应用赛博朋克风格 (V6) - 故障艺术与霓虹")
        print("7. 应用复古 DOS 风格 (V7) - CRT 终端效果")
        print("8. 应用波普艺术风格 (V8) - 孟菲斯/高对比")
        print("9. 应用瑞士设计风格 (V9) - 极简主义/网格布局")
        print("10. 应用新拟态风格 (V10) - 3D 软浮雕/现代简约")
        print("11. 应用蓝图风格 (V11) - 工程图纸/技术感")
        print("12. 应用禅意风格 (V12) - 自然/呼吸感/极简")
        print("0. 退出")
        print("-" * 40)
        
        choice = input("请选择风格 (0-12): ").strip()
        
        if choice == '1':
            print("\n正在应用统一风格...")
            os.system('python script/generate_v1_uniform.py')
            input("\n完成！按回车键继续...")
        elif choice == '2':
            print("\n正在应用多彩风格...")
            os.system('python script/generate_v2_colorful.py')
            input("\n完成！按回车键继续...")
        elif choice == '3':
            print("\n正在应用纹理风格...")
            os.system('python script/generate_v3_textured.py')
            input("\n完成！按回车键继续...")
        elif choice == '4':
            print("\n正在应用多布局风格...")
            os.system('python script/generate_v4_layouts.py')
            input("\n完成！按回车键继续...")
        elif choice == '5':
            print("\n正在应用独特布局风格...")
            os.system('python script/generate_v5_unique.py')
            input("\n完成！按回车键继续...")
        elif choice == '6':
            print("\n正在应用赛博朋克风格...")
            os.system('python script/generate_v6_cyberpunk.py')
            input("\n完成！按回车键继续...")
        elif choice == '7':
            print("\n正在应用复古 DOS 风格...")
            os.system('python script/generate_v7_retro.py')
            input("\n完成！按回车键继续...")
        elif choice == '8':
            print("\n正在应用波普艺术风格...")
            os.system('python script/generate_v8_popart.py')
            input("\n完成！按回车键继续...")
        elif choice == '9':
            print("\n正在应用瑞士设计风格...")
            os.system('python script/generate_v9_swiss.py')
            input("\n完成！按回车键继续...")
        elif choice == '10':
            print("\n正在应用新拟态风格...")
            os.system('python script/generate_v10_neumorphism.py')
            input("\n完成！按回车键继续...")
        elif choice == '11':
            print("\n正在应用蓝图风格...")
            os.system('python script/generate_v11_blueprint.py')
            input("\n完成！按回车键继续...")
        elif choice == '12':
            print("\n正在应用禅意风格...")
            os.system('python script/generate_v12_zen.py')
            input("\n完成！按回车键继续...")
        elif choice == '0':
            print("再见！")
            break
        else:
            print("无效的选择，请重试。")
            
if __name__ == "__main__":
    main()
