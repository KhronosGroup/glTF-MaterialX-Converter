
import os
import argparse

def get_files(input_path):
    '''
    Get all MaterialX files in a folder, or a single MaterialX file
    @param input_path: Path to the folder or file
    '''
    mtlx_files = []

    if os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            # Get files ending with .mtlx
            for file in files:
                if file.endswith(".mtlx"):
                    mtlx_files.append(os.path.join(root, file))
    elif input_path.endswith(".mtlx"):
        # Get absolute path
        input_path = os.path.abspath(input_path)
        mtlx_files.append(input_path)

    return mtlx_files

def render_folder(render_cmd, input_paths):
    '''
    Utilitie to use materialXView to render all .mtlx files in a folder
    @param render_cmd: MaterialXView command to render files
    @param input_paths: List of files to render
    '''
    # Get files ending with .mtlx
    for input_path in input_paths:
        if input_path.endswith(".mtlx"):
            print("Rendering: " + input_path)
            # Replace .mtlx with .png
            captureFilename = input_path.replace(".mtlx", ".png")
            cmd = render_cmd + f' --captureFilename {captureFilename} --material {input_path}'
            print(cmd)
            os.system(cmd)     
    
def main():
    # Add argument for MaterialXView command
    parser = argparse.ArgumentParser(description='Render MaterialX files in a folder')
    parser.add_argument('-c', '--renderCmd', type=str, help='MaterialXView command to render files')
    parser.add_argument('-r', '--resolution', type=int, help='Resolution of the render. Default is 256', default=256)
    parser.add_argument('input_path', type=str, help='Input path MaterialX file or folder containing MaterialX files')
    args = parser.parse_args()

    render_cmd = ''
    if args.renderCmd:
        render_cmd = args.renderCmd 
        
    # If not found try MATERIALX_VIEWER environment variable
    if not render_cmd:
        render_cmd = os.getenv('MATERIALX_VIEWER')
        if not render_cmd:
            print('MaterialXView command not found')
            return

    resolution = args.resolution
    render_cmd += f' --screenWidth {resolution} --screenHeight {resolution} '

    input_paths = get_files(args.input_path)
    if not input_paths:
        print('No MaterialX files found')
        return
    
    #print('Rendering: ' + input_paths)
    render_folder(render_cmd, input_paths)

if __name__ == "__main__":
    main()
