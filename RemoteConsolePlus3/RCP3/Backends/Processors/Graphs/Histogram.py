#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
import numpy as np
import matplotlib
import matplotlib.pyplot
from RCP3.Infrastructure import TmpFilesStorage

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        pass
    
    def GetParameters(self):
        """
        Returns a dictionary with object parameters, their values, 
        limits and ways to change them.
        """
        return {}
    
    def SetParameters(self, parameters):
        """
        Gets a dictionary with parameter values and
        update object parameters accordingly
        """
        pass
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """
        dataArray = np.asarray(message["Data"])

        
        fig = matplotlib.pyplot.figure(figsize=(6, 4), dpi=float(96))
        ax=fig.add_subplot(111)
        n, bins, patches = ax.hist(dataArray, bins=50)

        processedMessage = {"Stream":message["Stream"], "Info":message["Info"]} 
        
        filePath, link = TmpFilesStorage.NewTemporaryFile("png")
        fig.savefig(filePath,format='png')
        matplotlib.pyplot.close(fig)
        html = '<img src="http://{}" alt="Image should come here">'.format(link)
        processedMessage["Data"] = html
       
        self._parentNode.SendMessage(processedMessage)



        """        
        print len(message["Data"])
        import numpy as np
        import matplotlib.pyplot as plt
        
        x = np.array(message["Data"])
        
        num_bins = 50
        # the histogram of the data
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        plt.subplots_adjust(left=0.15)
        plt.show()
        """
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass