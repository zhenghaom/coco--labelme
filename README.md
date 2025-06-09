#脚本功能：
#该脚本的主要功能是将 COCO 数据集中的需要的类别数据转换为 LabelMe 格式的 JSON 文件，将图片和对应的 JSON 文件保存到指定目录。
#脚本流程
#设置路径：指定 COCO 数据集路径（dataDir）和保存生成文件的路径（saveDir），并创建用于保存图片的子目录（img_save_dir1 和 img_save_dir2）。
#定义类别和颜色映射：列出需要处理的动物类别（classes_names）以及对应的 LabelMe 格式颜色映射（colors）。
#检查图片：通过 check_image 函数检查每张图片是否满足以下条件之一：1.不包含人，只包含指定的动物类别（返回值为 1）。2.包含人且包含指定的动物类别（返回值为 2）。
#转换为 LabelMe 格式：对于满足条件的图片，调用 coco_to_labelme 函数将其对应的 COCO 格式注释转换为 LabelMe 格式的 JSON 文件。
#保存文件：保存到相应的目录，并统计满足条件的图片数量。
