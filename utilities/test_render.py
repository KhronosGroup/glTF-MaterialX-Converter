
import os
import argparse

def get_files(inputPath):
    '''
    Get all MaterialX files in a folder, or a single MaterialX file
    @param inputPath: Path to the folder or file
    '''
    mtlx_files = []

    if os.path.isdir(inputPath):
        for root, dirs, files in os.walk(inputPath):
            # Get files ending with .mtlx
            for file in files:
                if file.endswith(".mtlx"):
                    mtlx_files.append(os.path.join(root, file))
    elif inputPath.endswith(".mtlx"):
        # Get absolute path
        inputPath = os.path.abspath(inputPath)
        mtlx_files.append(inputPath)

    return mtlx_files

def renderFolder(renderCmd, inputPaths):
    '''
    Utilitie to use materialXView to render all .mtlx files in a folder
    @param renderCmd: MaterialXView command to render files
    @param inputPaths: List of files to render
    '''
    # Get files ending with .mtlx
    for inputPath in inputPaths:
        if inputPath.endswith(".mtlx"):
            print("Rendering: " + inputPath)
            # Replace .mtlx with .png
            captureFilename = inputPath.replace(".mtlx", ".png")
            cmd = renderCmd + f' --captureFilename {captureFilename} --material {inputPath}'
            print(cmd)
            os.system(cmd)     
    
def main():
    # Add argument for MaterialXView command
    parser = argparse.ArgumentParser(description='Render MaterialX files in a folder')
    parser.add_argument('-c', '--renderCmd', type=str, help='MaterialXView command to render files')
    parser.add_argument('-r', '--resolution', type=int, help='Resolution of the render. Default is 256', default=256)
    parser.add_argument('inputPath', type=str, help='Input path MaterialX file or folder containing MaterialX files')
    args = parser.parse_args()

    if args.renderCmd:
        renderCmd = args.renderCmd 
        
    resolution = args.resolution
    renderCmd += f' --screenWidth {resolution} --screenHeight {resolution} '

    # If not found try MATERIALX_VIEWER environment variable
    if not renderCmd:
        renderCmd = os.getenv('MATERIALX_VIEWER')
        if not renderCmd:
            print('MaterialXView command not found')
            return

    #renderCmd = 'D:/Work/materialx/ILM_materialx/build/installed/bin/MaterialXView.exe --screenWidth 256 --screenHeight 256 --captureFilename'
    inputPaths = get_files(args.inputPath)
    if not inputPaths:
        print('No MaterialX files found')
        return
    
    #print('Rendering: ' + inputPaths)
    renderFolder(renderCmd, inputPaths)

if __name__ == "__main__":
    main()